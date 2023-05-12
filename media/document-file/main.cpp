#include<bits/stdc++.h>

using namespace std;
using namespace std::chrono;
int dx[] = {1, 1, 0, -1, -1, -1, 0, 1};
int dy[] = {0, 1, 1, 1, 0, -1, -1, -1};
int dx4[] = {-1, 0, 0, 1};
int dy4[] = {0, -1, 1, 0};
#define _ 0
#define endl '\n'
#define ll long long
#define pii pair<int,int>
#define ull unsigned long long
#define all(X) (X).begin(),(X).end()
#define allr(X) (X).rbegin(),(X).rend()
#define Take(X) for (auto &it:(X)) cin >> it;
#define Out(X) for (auto &it:(X))cout << it << " ";
#define TAKE(X, S) for (auto &it:(X)) cin >> it, (S) += it;
#define Fast_IO ios::sync_with_stdio(false),cin.tie(nullptr),cout.tie(nullptr)
const int mod = 1e9 + 7;
const double pi = acos(-1);
const int N = 1e6 + 5;
const ll oo = LLONG_MAX;
const int OO = 0x7f7f7f7f;

ll Lcm(ll a, ll b) { return a * (b / __gcd(a, b)); }

int mult(int a, int b) { return (1LL * a * b) % mod; }

int mult(int a, int b, int mm) { return (1LL * a * b) % mm; }

int modSum(ll a, ll b) {
    a = (a % mod + mod) % mod, b = (b % mod + mod) % mod;
    return (a + b) % mod;
}

int modSub(ll a, ll b) { return modSum(a, -b); }

template<class T>
void debug(std::vector<T> &vect) {
    cerr << endl;
    for (auto x: vect)cerr << "'" << x << "' ";
    cerr << endl;
}

template<class T>
void debug(T argumentAmount, ...) {
    va_list arguments;
    va_start(arguments, argumentAmount);
    T parameter;
    for (int i = 0; i < argumentAmount; ++i) {
        parameter = va_arg(arguments, T);
        cerr << "'" << parameter << "' ";
    }
    cerr << endl;
    va_end(arguments);
    return;
}

/*___________________________________________________________________________*/
#define int ll

void blow_it() {
    int n, m, k, q, a, b, s;
    cin >> n >> m >> k >> q >> a >> b >> s;
    vector<int> h(n);
    Take(h);
    int dis = h[0] - 1;
    int bonus = dis / k * b;


}

void preprocess() {

}

int32_t main() {
    Fast_IO;
    /*freopen("input.in", "r", stdin);
    freopen("output.txt", "w", stdout);*/
    //cout << fixed << setprecision(12);
    int t = 1, cases = 1;
    //cin >> t;
    //std::chrono::high_resolution_clock::time_point start = std::chrono::high_resolution_clock::now();
    preprocess();
    while (t--) {
        //cout << "Case #" << cases++ << ':' << endl;
        blow_it();
    }
    //std::chrono::high_resolution_clock::time_point end = std::chrono::high_resolution_clock::now();
    //cerr << "Time : " << (end - start).count() / (1000000.0l) << " ms \n";
    return (0 ^ _ ^ 0);
}