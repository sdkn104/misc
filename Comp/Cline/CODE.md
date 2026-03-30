# 内部構造の情報

- https://zenn.dev/gvatech_blog/articles/11bc7181afff69
- https://note.com/naru_jpn/n/n67ecfdd12cf9
- https://qiita.com/straygizmo/items/706778f8ddd3d59f0f87
- [cline-main\.clinerules\cline-overview.md](https://github.com/cline/cline/blob/main/.clinerules/cline-overview.md)


# 内部構造の解析


```
src/core/controller/index.ts
export class Controller {
	async initTask(task?: string, ...) {
		this.task = new Task({
		...
        this.task.startTask(task, images, files)

```

### TASK LOOP
src/core/task/index.ts
```javascript
export class Task {

    public async startTask(task?: string, images?: string[], files?: string[]): Promise<void> {
		await this.initiateTaskLoop(userContent)
        
    ...

	private async initiateTaskLoop(userContent: ClineContent[]): Promise<void> {
		let nextUserContent = userContent
		let includeFileDetails = true
		while (!this.taskState.abort) {
			const didEndLoop = await this.recursivelyMakeClineRequests(nextUserContent, includeFileDetails)
			includeFileDetails = false // we only need file details the first time

			//  The way this agentic loop works is that cline will be given a task that he then calls tools to complete. unless there's an attempt_completion call, we keep responding back to him with his tool's responses until he either attempt_completion or does not use anymore tools. If he does not use anymore tools, we ask him to consider if he's completed the task and then call attempt_completion, otherwise proceed with completing the task.

			//const totalCost = this.calculateApiCost(totalInputTokens, totalOutputTokens)
			if (didEndLoop) { // 間違いがなければ終了する？
				// For now a task never 'completes'. This will only happen if the user hits max requests and denies resetting the count.
				//this.say("task_completed", `Task completed. Total API usage cost: ${totalCost}`)
				break
			}
			nextUserContent = [
				{
					type: "text",
					text: formatResponse.noToolsUsed(this.useNativeToolCalls),
				},
			]
			this.taskState.consecutiveMistakeCount++
		}
    }
    
    async recursivelyMakeClineRequests(userContent: ClineContent[], includeFileDetails) {

        const stream = this.attemptApiRequest(previousApiReqIndex) // yields only if the first chunk is successful, otherwise will allow the user to retry the request (most likely due to rate limit error, which gets thrown on the first chunk)

        while (true) {
            const chunk = await streamCoordinator.nextChunk()

            switch (chunk.type) {
                case "reasoning": {
                    reasonsHandler.processReasoningDelta({
                        id: chunk.id,
                        reasoning: chunk.reasoning,
                        signature: chunk.signature,
                        chunk.details,
                        redacted_data: chunk.redacted_data,
                    })
                    await this.scheduleAssistantPresentation(// present to user
                        "reasoning",
                        this.getPresentationPriorityForChunk({ chunkType: "reasoning", hadVisibleAssistantContent }),
                    )
                    break
                }
                case "tool_calls": {
                    toolUseHandler.processToolUseDelta(
                        {
                            id: chunk.tool_call.function?.id,
                            type: "tool_use",
                            name: chunk.tool_call.function?.name,
                            input: chunk.tool_call.function?.arguments,
                            signature: chunk?.signature,
                        },
                        chunk.tool_call.call_id,
                    )
                    await this.processNativeToolCalls(assistantTextOnly, toolUseHandler.getPartialToolUsesAsContent())
                    await this.scheduleAssistantPresentation( // present to user, tool call
                        "tool",
                        this.getPresentationPriorityForChunk({ chunkType: "tool_calls", hadVisibleAssistantContent }),
                    )
                    break
                }
                case "text": {
                    assistantMessage += chunk.text
                    this.taskState.assistantMessageContent = parseAssistantMessageV2(assistantMessage)

                    await this.scheduleAssistantPresentation(// present to user
                        "text",
                        this.getPresentationPriorityForChunk({ chunkType: "text", hadVisibleAssistantContent }),
                    )
                    break
                }
            }
            if (this.taskState.abort) {
                break // aborts the stream
            }
            if (this.taskState.didRejectTool) {
                break
            }
        }
    	await pWaitFor(() => this.taskState.userMessageContentReady)
        const recDidEndLoop = await this.recursivelyMakeClineRequests(this.taskState.userMessageContent)

    }

	private async scheduleAssistantPresentation(...): Promise<void> {
		if (this.presentationSchedulingDisabled) {
			await this.presentationScheduler.flushNow().catch((error) => {
				Logger.warn(`[Task] Failed immediate presentation flush: ${error}`)
			})
			return
		}
		// Immediate semantic boundaries: first visible token, tool transitions, finalization, and cleanup drains.
		Logger.debug(`[Task ${this.taskId}] schedule assistant presentation (${trigger}, ${priority})`)
		this.presentationScheduler.requestFlush(priority) // include call of executeTool()
	}

	constructor(params: TaskParams) {
		this.presentationScheduler = new TaskPresentationScheduler({
			flush: () => this.presentAssistantMessage(),
		})

	async presentAssistantMessage() {
		switch (block.type) {
			case "tool_use":
				await this.toolExecutor.executeTool(block)
```



### LLM API CALL
src/core/task/index.ts
```javascript
export class Task {
	async *attemptApiRequest(previousApiReqIndex: number): ApiStream {
		const promptContext: SystemPromptContext = {
            ...
        }
		const { systemPrompt, tools } = await getSystemPrompt(promptContext)
		const stream = this.api.createMessage(systemPrompt, contextManagementMetadata.truncatedConversationHistory, tools)
    
    constructor() {
		this.api = buildApiHandler(effectiveApiConfiguration, mode)
```

src\core\prompts\system-prompt\index.ts
```javascript
export async function getSystemPrompt(context: SystemPromptContext) {
	const registry = PromptRegistry.getInstance()
	const systemPrompt = await registry.get(context)
	const tools = context.enableNativeToolCalls ? registry.nativeTools : undefined
	return { systemPrompt, tools }
}
```

src\core\prompts\system-prompt\registry\PromptRegistry.ts
```javascript
export class PromptRegistry {
	/**
	 * Get prompt by matching against all registered variants
	 */
	async get(context: SystemPromptContext): Promise<string> {
		const variant = this.getVariant(context)

		// Hacky way to get native tools for the current variant - it's bad and ugly
		this.nativeTools = ClineToolSet.getNativeTools(variant, context)

		const builder = new PromptBuilder(variant, context, this.components)
		return await builder.build()
	}
```
### MESSAGES
```typescript
class Task {
	public async startTask(task?: string, images?: string[], files?: string[]): Promise<void> {
		await this.initTask(prompt)  ---> 

		....

		const userContent: ClineUserContent[] = [
			{
				type: "text",
				text: `<task>\n${task}\n</task>`,  <--- task=上記のprompt
			},
			...imageBlocks,
		]
		if (files && files.length > 0) {
			const fileContentString = await processFilesIntoText(files)
            userContent.push({
                type: "text",
                text: fileContentString,
            })
		}
        if (taskStartResult.contextModification) {
            const contextText = taskStartResult.contextModification.trim()
            userContent.push({
                type: "text",
                text: `<hook_context source="TaskStart">\n${contextText}\n</hook_context>`,
            })
        }
		await this.initiateTaskLoop(userContent)

	async recursivelyMakeClineRequests(userContent: ClineContent[], includeFileDetails = false) {
		if (environmentDetails) {
			userContent.push({ type: "text", text: environmentDetails })
		}
		await this.messageStateHandler.addToApiConversationHistory({
			role: "user",
			content: userContent,
			ts: Date.now(),
		})
		await this.messageStateHandler.updateClineMessage(lastApiReqIndex, {
			text: JSON.stringify({
				request: userContent.map((block) => formatContentBlockToMarkdown(block)).join("\n\n"),
			} satisfies ClineApiReqInfo),
		})
    }
	async *attemptApiRequest(previousApiReqIndex: number): ApiStream {
		const promptContext: SystemPromptContext = {
            ...
        }
		const { systemPrompt, tools } = await getSystemPrompt(promptContext)
		const contextManagementMetadata = await this.contextManager.getNewContextMessagesAndMetadata(
			this.messageStateHandler.getApiConversationHistory(),
			this.messageStateHandler.getClineMessages(),
		)
		const stream = this.api.createMessage(systemPrompt, contextManagementMetadata.truncatedConversationHistory, tools)
```



### TOOL CALL
src\core\task\ToolExecutor.ts
```
export class ToolExecutor {
	public async executeTool(block: ToolUse): Promise<void> {
		await this.execute(block)
	}


	private async execute(block: ToolUse): Promise<boolean> {
			await this.handleCompleteBlock(block, config)

    /**
	 * Handle complete block execution.
	 *
	 * This is the main execution flow for a tool:
	 * 1. Execute the actual tool (tool handlers now run PreToolUse hooks post-approval)
	 * 2. Run PostToolUse hooks (if enabled) - cannot block, only observe
	 * 3. Add hook context modifications to the conversation
	 * 4. Update focus chain tracking
	 */
	private async handleCompleteBlock(block: ToolUse, config: any): Promise<void> {
```