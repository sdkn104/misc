package com.example.springbootrestapi;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class SampleController {
    @GetMapping("/sample")
    public SampleDto getSample() {
        return new SampleDto("OK");
    }
}
