#include <bits/stdc++.h>
using namespace std;

int main(){
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int N=3; //if(!(cin>>N)) return 0;
	if(N==1){ cout<<0<<"\n"; return 0; }

	int LIM = 2*N + 5;
	vector<int> fact(LIM);
	fact[0]=1;
	for(int i=1;i<LIM;i++) fact[i] = fact[i-1] * i;

	auto C = [&](int n,int k)->int{
		if(k<0 || k>n) return int(0);
		return fact[n] / (fact[k] * fact[n-k]);
	};

	int cells = N*N;
	vector<int> sval(cells);
	auto idx = [&](int i,int j){ return i*N + j; };

	for(int i=0;i<N;i++){
		for(int j=0;j<N;j++){
			int t = i + j;
			// s = C[2N - i - j][N - i] + C[i+j+2][i+1] - 4
			int s1 = C(2*N - i - j, N - i);
			int s2 = C(i + j + 2, i + 1);
			int s = s1 + s2 - 4;
			sval[idx(i,j)] = s;
		}
	}

	int total_s = 0;
	for(int k=0;k<cells;k++) total_s += sval[k];
	int target = total_s / 2; // integer

	// greedy fill by descending sval
	vector<int> order(cells);
	for(int i=0;i<cells;i++) order[i]=i;
	sort(order.begin(), order.end(), [&](int a,int b){ return sval[a] > sval[b]; });

	vector<char> pick(cells,0);
	int cur = 0;
	for(int id : order){
		if(cur + sval[id] <= target){ pick[id]=1; cur += sval[id]; }
	}

	// quick randomized local search to try reach exact target
	mt19937_64 rng(chrono::high_resolution_clock::now().time_since_epoch().count());
	auto now = chrono::high_resolution_clock::now;
	double TL = 1.8; // seconds
	auto t0 = now();

	auto absdiff = [&](const int &a, const int &b){ return (a>b? a-b : b-a); };

	while((double)chrono::duration_cast<chrono::duration<double>>(now()-t0).count() < TL){
		if(cur == target) break;
		// try single flip moves
		int i = rng() % cells;
		int newcur = cur + (pick[i] ? -sval[i] : sval[i]);
		if(absdiff(newcur, target) < absdiff(cur, target)){
			pick[i] = !pick[i];
			cur = newcur;
			continue;
		}
		// try pair flip to make exact if possible: try a few random j
		for(int trial=0; trial<6; ++trial){
			int j = rng() % cells;
			if(i==j) continue;
			int delta = (pick[i]? -sval[i] : sval[i]) + (pick[j]? -sval[j] : sval[j]);
			int cand = cur + delta;
			if(absdiff(cand,target) < absdiff(cur,target)){
				pick[i] = !pick[i]; pick[j] = !pick[j]; cur = cand; break;
			}
		}
	}

	// if not found, try a few random restarts of greedy
	if(cur != target){
		for(int rep=0; rep<20 && cur!=target; ++rep){
			// randomize order slightly
			shuffle(order.begin(), order.end(), rng);
			fill(pick.begin(), pick.end(), 0);
			cur = 0;
			for(int id: order){ if(cur + sval[id] <= target){ pick[id]=1; cur += sval[id]; } }
			auto tstart = now();
			while((double)chrono::duration_cast<chrono::duration<double>>(now()-tstart).count() < 0.08){
				if(cur==target) break;
				int i = rng()%cells;
				int newcur = cur + (pick[i] ? -sval[i] : sval[i]);
				if(absdiff(newcur, target) < absdiff(cur, target)){
					pick[i] = !pick[i]; cur = newcur; continue;
				}
			}
		}
	}

	// As a last resort, if still not equal (very unlikely), output a simple pattern
	if(cur != target){
		// fallback: alternate checkerboard
		for(int i=0;i<N;i++){
			for(int j=0;j<N;j++) cout << ((i+j)&1);
			cout << '\n';
		}
		return 0;
	}

	// print grid
	for(int i=0;i<N;i++){
		for(int j=0;j<N;j++) cout << (pick[idx(i,j)]? '1' : '0');
		cout << '\n';
	}
	return 0;
}

