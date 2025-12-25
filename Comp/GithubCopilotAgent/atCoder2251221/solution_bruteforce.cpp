#include <bits/stdc++.h>
using namespace std;

int main(){
	const int N = 3;
	// precompute small binomials up to 4
	long long C[6][6] = {};
	for(int n=0;n<6;n++){
		C[n][0]=C[n][n]=1;
		for(int k=1;k<n;k++) C[n][k]=C[n-1][k-1]+C[n-1][k];
	}

	auto paths = [&](int r1,int c1,int r2,int c2)->long long{
		int dr=r2-r1, dc=c2-c1;
		if(dr<0||dc<0) return 0;
		if(dr==0 && dc==0) return 0;
		return C[dr+dc][dr];
	};

	// brute force all 2^9 assignments
	for(int mask=0; mask < (1<< (N*N)); ++mask){
		int a[N][N];
		for(int i=0;i<N;i++) for(int j=0;j<N;j++){
			int idx = i*N + j;
			a[i][j] = (mask>>idx) & 1;
		}
		long long f0=0, f1=0;
		for(int r1=0;r1<N;r1++) for(int c1=0;c1<N;c1++){
			for(int r2=r1;r2<N;r2++) for(int c2=c1;c2<N;c2++){
				if(r1==r2 && c1==c2) continue;
				long long p = paths(r1,c1,r2,c2);
				if(a[r1][c1]==a[r2][c2]){
					if(a[r1][c1]==0) f0 += p;
					else f1 += p;
				}
			}
		}
		if(f0==f1){
			for(int i=0;i<N;i++){
				for(int j=0;j<N;j++) cout<<a[i][j];
				cout<<"\n";
			}
            cout << "-----\n";
			return 0;
		}
	}
	// should not happen for 3x3, but print fallback
	for(int i=0;i<N;i++){ cout<<string(N,'0')<<"\n"; }
	return 0;
}

