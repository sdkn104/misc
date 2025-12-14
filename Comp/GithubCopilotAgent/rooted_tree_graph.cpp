#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

class Graph {
public:
    struct Edge { int to, id; };

    int N, M, H;
    vector<int> x, y, A;
    vector<vector<Edge>> adj;
    vector<bool> used_vertex;
    vector<bool> used_edge;
    ll total_score = 0;

    Graph() : N(0), M(0), H(0) {}

    void readInput(istream &in) {
        in >> N >> M >> H;
        x.assign(N, 0);
        y.assign(N, 0);
        A.assign(N, 0);
        adj.assign(N, {});
        used_vertex.assign(N, false);
        used_edge.assign(M, false);

        for (int i = 0; i < N; ++i) {
            in >> x[i] >> y[i] >> A[i];
        }
        for (int i = 0; i < M; ++i) {
            int u, v;
            in >> u >> v;
            adj[u].push_back({v, i});
            adj[v].push_back({u, i});
        }
    }

    // root から BFS を行い、その根付き木の見栄えを計算して頂点をマーク
    ll buildTree(int root) {
        vector<int> height(N, -1);
        queue<int> q;
        vector<char> in_tree(N, 0);

        q.push(root);
        height[root] = 0;
        in_tree[root] = 1;
        ll appearance = 0;

        while (!q.empty()) {
            int v = q.front(); q.pop();
            appearance += (ll)(height[v] + 1) * A[v];

            if (height[v] >= H) continue;

            for (const Edge &e : adj[v]) {
                int u = e.to;
                if (!in_tree[u] && !used_vertex[u]) {
                    in_tree[u] = 1;
                    height[u] = height[v] + 1;
                    used_edge[e.id] = true;
                    q.push(u);
                }
            }
        }

        for (int i = 0; i < N; ++i) if (in_tree[i]) used_vertex[i] = true;
        return appearance;
    }

    int chooseBestRoot() const {
        int best = -1;
        for (int i = 0; i < N; ++i) {
            if (!used_vertex[i]) {
                if (best == -1 || A[i] > A[best]) best = i;
            }
        }
        return best;
    }

    void processAllRoots() {
        while (true) {
            int r = chooseBestRoot();
            if (r == -1) break;
            ll sc = buildTree(r);
            total_score += sc;
        }
    }

    void printScore(ostream &out) const {
        out << (1 + total_score) << '\n';
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    Graph g;
    g.readInput(cin);
    g.processAllRoots();
    g.printScore(cout);

    return 0;
}
