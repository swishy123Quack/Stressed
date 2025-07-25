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
vector<string> tokenize(ifstream &f){
    string line;
    vector<string> tokens;

    while (getline(f, line)){
        istringstream iss(line);
        string token;
        while (iss >> token) 
            tokens.push_back(token);
    }

    return tokens;
}

string ordinal(int n){
    int last_two = n % 100;
    int last = n % 10;

    string suffix;
    if (last_two >= 11 && last_two <= 13)
        suffix = "th"; 
    else if (last == 1)
        suffix = "st";
    else if (last == 2)
        suffix = "nd";
    else if (last == 3)
        suffix = "rd";
    else
        suffix = "th";

    return to_string(n) + suffix;
}

string trim(string s){
    int max_char = 50;
    string res = "";

    for (int i = 0; i < min((int)s.size(), max_char); i++)
        res += s[i];
    if (res.size() > max_char)
        res += "...";
    return res;
}

int main(int argc, char *argv[]){
    ifstream sol(argv[1]);
    ifstream brute(argv[2]);

    vector<string> token1 = tokenize(sol), token2 = tokenize(brute);
    for (int i = 0; i < max(token1.size(), token2.size()); i++){
        if (i == token1.size()){
            print("Missing", ordinal(i + 1), "token from solution: Expected", trim(token2[i]) + ',', "found EOL instead");
            return 0;
        }
        if (i == token2.size()){
            print("Missing", ordinal(i + 1), "token from brute: Expected EOL, found", trim(token1[i]), "instead");
            return 0;
        }
        if (token1[i] != token2[i]){
            print(ordinal(i + 1), "token mismatch: Expected", trim(token2[i]) + ',', "found", trim(token1[i]), "instead");
            return 0;
        } 
    }
    return 0;
}