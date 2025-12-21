#include <bits/stdc++.h>
using namespace std;


#define MAX(a,b) ((a)>(b)?(a):(b))
#define MIN(a,b) ((a)<(b)?(a):(b))

class Machine {
public:
    int level, id;
    long long cost_base;
    long long production; // For level 0 only
    
    Machine(int l, int i, long long cb, long long prod = 0)
        : level(l), id(i), cost_base(cb), production(prod) {}
};

class State {
public:
    int N, L;
    long long apples;
    vector<long long> A; // Production ability for level 0
    vector<vector<long long>> C; // Cost matrix
    vector<vector<long long>> B; // Count of machines
    vector<vector<long long>> P; // Power of machines
    
    State(int n, int l, long long k)
        : N(n), L(l), apples(k),
          A(n), C(l, vector<long long>(n)),
          B(l, vector<long long>(n, 1)),
          P(l, vector<long long>(n, 0)) {}
    
    long long getUpgradeCost(int i, int j) const {
        return C[i][j] * (P[i][j] + 1);
    }

    long long getUpgradeCost2(int i, int j) const {
        long long cost = 0;
        for(int l = 0; l < i; l++) {
            if( P[l][j] == 0 ) {
                cost += getUpgradeCost(l, j);
            }
        }
        cost += getUpgradeCost(i, j);
        return cost;
    }

    bool canUpgrade(int i, int j) const {
        return getUpgradeCost(i, j) <= apples;
    }
    
    void upgradeMachine(int i, int j) {
        long long cost = getUpgradeCost(i, j);
        apples -= cost;
        P[i][j]++;
    }

    void upgradeMachine2(int i, int j) {
        for(int l = 0; l < i; l++) {
            if( P[l][j] == 0 ) {
                upgradeMachine(l, j);
            }
        }
        upgradeMachine(i, j);
    }

    long long calculateApples() {
        int a = 0;
        for (int j = 0; j < N; j++) {
                // Level 0: produce apples
                a += A[j] * B[0][j] * P[0][j];
        }
        return a;
    }

    void produceApples() {
        for (int i = 0; i < L; i++) {
            for (int j = 0; j < N; j++) {
                if (i == 0) {
                    // Level 0: produce apples
                    apples += A[j] * B[i][j] * P[i][j];
                } else {
                    // Level i >= 1: multiply B[i-1][j]
                    B[i-1][j] += B[i][j] * P[i][j];
                }
            }
        }
    }
    
    long long calculatePredictedGain(int i, int j, int dt) const {
        // Calculate predicted gain G_{i,j}(dt) at turn dt after upgrading machine j^i
        switch (i) {
            case 0:
                // G_0,j(t) = A_j * B_0,j
                return A[j] * B[i][j];
            
            case 1:
                // G_1,j(t) = A_j * P_0,j * t
                return A[j] * P[0][j] * dt;
            
            case 2:
                // G_2,j(t) = A_j * P_1,j * B_2,j * P_0,j * t(t-1)/2  (t > 0)
                if (dt == 0) return 0;
                return A[j] * P[1][j] * B[i][j] * P[0][j] * dt * (dt - 1) / 2;
            
            case 3:
                // G_3,j(t) = A_j * P_0,j * P_1,j * B_3,j * t(t-1)(t-2)/6  (t > 1)
                if (dt <= 1) return 0;
                return A[j] * P[0][j] * P[1][j] * B[i][j] * dt * (dt - 1) * (dt - 2) / 6;
            
            default:
                return 0;
        }
    }

    State deepCopy() const {
        // Return a deep copy of this State. std::vector copy is deep for elements.
        State s = *this;
        return s;
    }
};

class Simulator {
private:
    State state;
    int T;
    
    pair<int, int> findBestUpgrade(int turn) {
        long long applesPerTurn = state.calculateApples();
        cout << "# Apples per turn: " << applesPerTurn << " apples " << state.apples << "\n";

        int best_i = -1, best_j = -1;
        double best_value = -100;

        for (int i = 0; i < state.L; i++) {
            for (int j = 0; j < state.N; j++) {
                long long upgrade_cost = state.getUpgradeCost2(i, j);
                int fusoku = MAX(0, upgrade_cost - state.apples);
                int upgrade_turn = turn + fusoku / MAX(1, applesPerTurn);
                if( fusoku % MAX(1, applesPerTurn) == 0 && fusoku != 0 ) upgrade_turn--;
                if ( upgrade_turn >= T && applesPerTurn != 0) continue;
                //if( upgrade_turn > turn ) continue;
                if (upgrade_cost > state.apples + applesPerTurn * (T - turn) ) continue;
                //if (!state.canUpgrade(i, j)) continue;
                upgrade_turn = MIN(upgrade_turn, T-1);

                double gain = simulateFinalAppleDifference(i, j, upgrade_turn);
                double value = gain * ((double)(T - turn) / (double)MAX(1, upgrade_turn - turn + 1));
                //double value = simulateFinalAppleDifference2(i, j, upgrade_turn);
                //cout << "# Simulated cummulative gain for " << i << " " << j << " c:" << cumm << " g:" << gain << "\n";

                cout << "# " << turn << ": " << i << " " << j << " g:" << gain << " v:" << value << " t:" << (upgrade_turn-turn) << "\n";
                //if (!state.canUpgrade(i, j)) cout << "# (not affordable)\n";


                if (value > best_value) {
                    best_value = value;
                    best_i = i;
                    best_j = j;
                }
            }
        }

        cout << "# Best upgrade candidate: " << best_i << " " << best_j << " with value " << best_value << "\n";
        if (best_i != -1 && !state.canUpgrade(best_i, best_j)) {
            return {-1, -1};
        }

        return {best_i, best_j};
    }
    
    // DFS exploration helper (no lambda) that explores sequences of choices for same id `j`.
    void dfsExplore(long long apples0, int t0, int remaining, State s, int tcur, vector<pair<int,int>> &seq,
                    long long &best_final, int &best_i, int &best_j, int Tlocal) const {
        if (remaining == 0) {
            State ss = s.deepCopy();
            int tt = tcur;
            while (tt < Tlocal) { ss.produceApples(); ++tt; }
            long long finalApples = ss.apples;
            //cout << "# Final apples:" << finalApples << "\n";
            long long value = (finalApples - apples0) * (Tlocal - t0) / (tcur - t0 + 1);    
            if (value > best_final) {
                best_final = value;
                best_i = seq.empty() ? -1 : seq[0].first;
                best_j = seq.empty() ? -1 : seq[0].second;
            }
            return;
        }


        for (int lvl = 0; lvl < s.L; ++lvl) {
            for (int n = 0; n < s.N; ++n) {
                State ns = s.deepCopy();
                int nt = tcur;
                while (nt < Tlocal && !ns.canUpgrade(lvl, n)) {
                    ns.produceApples();
                    ++nt;
                }
                if (nt >= Tlocal) continue;
                ns.upgradeMachine(lvl, n);
                ns.produceApples();
                ++nt;

                //cout << "# -dep: " << remaining << " l:" << lvl << " n:" << n << " tcur: " << nt << " appls:" << ns.apples << "\n";
                seq.push_back({lvl, n});
                dfsExplore(apples0, t0, remaining - 1, ns, nt, seq, best_final, best_i, best_j, Tlocal);
                seq.pop_back();
            }
        }
    }

    pair<int, int> findBestUpgrade2(int turn, int depth) {
        int best_i = -1, best_j = -1;
        long long best_final = -1; // pick minimal final apples

        //int depth = min(3, T - turn); // depth can be tuned

        State s0 = state.deepCopy();
        vector<pair<int,int>> seq;
        dfsExplore(s0.apples, turn, depth, s0, turn, seq, best_final, best_i, best_j, T);
        cout << "# Choise:" << best_i << " " << best_j << "\n";

        if (best_i == -1) return {-1, -1};
        if (!state.canUpgrade(best_i, best_j)) return {-1, -1};
        return {best_i, best_j};
    }

    double calculateUpgradeValue(int i, int j) {
        if (i == 0) {
            // Direct apple production
            return (double)state.A[j] * state.B[i][j] / (double)(state.P[i][j] + 1);
        } else {
            // Multiplication effect - harder to estimate
            // Use a heuristic based on the current B[i-1][j]
            return (double)state.B[i-1][j] * (state.P[i][j] + 1) / log(state.C[i][j] + 1);
        }
    }
    
    double calculateCumulativeGain(int i, int j, int upgrade_turn, int max_turns = -1) const {
        // Calculate cumulative gain from turn (upgrade_turn+1) to turn (T-1)
        // after upgrading machine j^i at upgrade_turn
        long long total_gain = 0;
        max_turns = (max_turns == -1) ? T : max_turns;
        for (int t = upgrade_turn; t < max_turns; t++) {
            total_gain += state.calculatePredictedGain(i, j, t-upgrade_turn);
        }
        return (double)total_gain;
    }

public:
    Simulator(int n, int l, int t, long long k)
        : state(n, l, k), T(t) {}

    State cloneState() const {
        return state.deepCopy();
    }

    // Simulate from current simulator.state for two branches:
    // 1) upgrade machine (i,j) at `current_turn` then do nothing for remaining turns
    // 2) do nothing for all remaining turns
    // Returns (final_apples_with_upgrade - final_apples_without_upgrade)
    long long simulateFinalAppleDifference(int i, int j, int current_turn) const {
        // Branch A: with upgrade at current_turn
        State sA = cloneState();
        sA.upgradeMachine2(i, j);
        for (int t = current_turn; t < T; ++t) {
            sA.produceApples();
        }

        // Branch B: do nothing
        State sB = cloneState();
        for (int t = current_turn; t < T; ++t) {
            sB.produceApples();
        }

        return sA.apples - sB.apples;
    }

    long long simulateFinalAppleDifference2(int i, int j, int current_turn) const {
        // Branch A: with upgrade at current_turn
        State sA = cloneState();
        for (int t = current_turn; t < T; ++t) {
            if( sA.canUpgrade(i, j) ) {
                if( sA.calculatePredictedGain(i, j, T-t) > sA.getUpgradeCost(i, j) ) {
                    sA.upgradeMachine(i, j);
                }
            }
            sA.produceApples();
        }

        // Branch B: do nothing
        State sB = cloneState();
        for (int t = current_turn; t < T; ++t) {
            sB.produceApples();
        }

        return sA.apples - sB.apples;
    }


    void readInput() {
        for (int i = 0; i < state.N; i++) {
            cin >> state.A[i];
        }
        
        for (int i = 0; i < state.L; i++) {
            for (int j = 0; j < state.N; j++) {
                cin >> state.C[i][j];
            }
        }
    }
    
    void runSimulation() {
        for (int turn = 0; turn < T; turn++) {
            auto [best_i, best_j] = findBestUpgrade2(turn, 2);
            
            if (best_i != -1) {
                state.upgradeMachine(best_i, best_j);
                cout << best_i << " " << best_j << "\n";
            } else {
                cout << "-1\n";
            }
            
            state.produceApples();
        }
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int N, L, T, K;
    cin >> N >> L >> T >> K;
    
    Simulator simulator(N, L, T, K);
    simulator.readInput();
    simulator.runSimulation();
    
    return 0;
}
