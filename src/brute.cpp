#include <iostream>
#include <algorithm>
#include <vector>
#include <random>
#include <chrono>
#include <set>
#include <map>
#include <stack>
#include <functional>
#include <iomanip>
#include <queue>
#include <cassert>
#include <complex>
#include <cstring>
#include <memory>
#include <bitset>
#include <sstream>
#include <cmath>
#include <numeric>
#include <numbers>
#include <fstream>
 
using namespace std;
 
#ifndef template
#ifndef define
 
#pragma GCC target("popcnt")
 
#define ll long long
#define ld long double
#define pl pair<ll, ll>
#define pi pair<int, int>
#define nl cout << '\n';
#define x first
#define y second 
#define cbit(x) __builtin_popcountll(x)
#define uid(a, b) uniform_int_distribution<ll>(a, b)(rng) 
#define siz(x) (int)x.size()
#define all(x) (x).begin(), (x).end() 
 
#endif
 
#ifndef print
void print(size_t x) {cout << x << ' ';}
void print(int x) {cout << x << ' ';}
void print(long long x) {cout << x << ' ';}
void print(float x) {cout << x << ' ';}
void print(long double x) {cout << x << ' ';}
void print(char x) {cout << x << ' ';}
void print(const char* x) {cout << x << ' ';}
void print(bool x) {cout << x << ' ';}
void print(string &x) {cout << x << ' ';}
 
template<typename T, typename V>
void print(pair<T, V> &p) {print(p.x); print(p.y);}
template<typename T>
void print(vector<T> v) {for (int i = 0; i < v.size(); i++) print(v[i]);}
template<typename T>
void print(vector<vector<T>> v) {
    for (int i = 0; i < v.size(); i++){
        for (int j = 0; j < v[i].size(); j++)
            print(v[i][j]);
        nl;
    }
}
template <typename T, typename... V>
void print(T t, V&&... v) {print(t); print(v...);}
 
#endif
 
#ifndef read
void read(int &x) {cin >> x;}
void read(long long &x) {cin >> x;}
void read(unsigned &x) {cin >> x;}
void read(unsigned long long &x) {cin >> x;}
void read(float &x) {cin >> x;}
void read(long double &x) {cin >> x;}
void read(char &x) {cin >> x;}
void read(string &x) {cin >> x;}
void read(bool &x) {cin >> x;}
 
template<typename T> 
void read(vector<T> &v) {
    for (int i = 0; i < v.size(); i++)
        read(v[i]);
}
template <typename T, typename... V>
void read(T &t, V&... v) {read(t); read(v...);}
#endif
 
mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());
template<class T> bool maxi(T& a, const T& b) {
    return a < b ? a = b, 1 : 0;
}
template<class T> bool mini(T& a, const T& b) {
    return a > b ? a = b, 1 : 0;
}
template<class... Args>
auto vec(size_t n, Args&&... args) {
    if constexpr(sizeof...(args) == 1)
        return vector(n, args...);
    else
        return vector(n, vec(args...));
}
 
#endif
 
using namespace std;
const ll inf = 1e9;
const ll def = 1e6+1;
ll mod = 998244353;

struct modu{
    ll val;
    modu(ll x){
        val = x;
        val %= mod;
        if (val < 0) val += mod;    
    }
    modu(){ val = 0; }
 
    operator ll() const { return val; }
    modu operator+(modu const& other){ return val + other.val; }
    modu operator-(modu const& other){ return val - other.val; }
    modu operator*(modu const& other){ return val * other.val; }
    modu operator/(modu const& other){ return *this * other.inv(); }
    modu operator+=(modu const& other) { *this = *this + other; return *this; }
    modu operator-=(modu const& other) { *this = *this - other; return *this; }
    modu operator*=(modu const& other) { *this = *this * other; return *this; }
    modu operator/=(modu const& other) { *this = *this / other; return *this; }
    modu operator++(int) {modu tmp = *this; *this += 1; return tmp;}
    modu operator++() {*this += 1; return *this;}
    modu operator--(int) {modu tmp = *this; *this -= 1; return tmp;}
    modu operator--() {*this -= 1; return *this;}
    modu operator-() {return modu(-val);}
    friend ostream& operator<<(ostream& os, modu const& m) { return os << m.val; }
    friend istream& operator>>(istream& is, modu & m) { return is >> m.val; }
 
    modu pow(ll x) const{
        if (x == 0) 
            return 1;
        if (x % 2 == 0){
            modu tmp = pow(x / 2);
            return tmp * tmp;
        }
        else
            return pow(x - 1) * *this;
    }
 
    modu inv() const{ return pow(mod - 2); }
};

void solve(){  
    int n, m;
    read(n, m);
    for (int i = 0; i < n; i++) for (int j = 0; j < m; j++){
        print(i * m + j + uid(0, 1));
        if (j == m - 1)
            nl;
    }
}         

/*
bruh
4 5 6 -> 1 2 3 -> 3 4 5 -> 1 1 2 3 -> 4 5 6
4 6 8 -> 1 3 5 -> 4 6 8 
2 7 9 12 -> 1 4 6 11 -> x

1 + (1 + a4 - a3) + (1 + a4 - a2) + (1 + a4 - a1) = (an + 1) * n - sn

(an + 1) * n - sn - (1 + an - a1) <= a1
=> (an + 1) * (n - 1) - s(n - 1) - an <= 0


0 1 0 1 0 1
0 0 1 0 0 1
0 0 0 1 0 0 
1 1
*/

int32_t main(){
    ios_base::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);

    // if (ifstream("input.txt").good()){
    //     freopen("input.txt", "r", stdin);
    //     freopen("output.txt", "w", stdout);
    // }
 
    int t;
    t = 1;

    while (t--){
        solve();
        nl;
    }
}