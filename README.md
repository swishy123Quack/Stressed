# Stressed
A competitive programming command line stress tester

## WARNING: Mac/Unix support is NOT supported! Only run this on Windows.

## Summary:
- This is my personal stress tester for competitive programming, so most of the features in this are tailored to my needs. If you find these helpful, feel free to use it! But don't expect it to have everything you need.

## Main features:
- Parallel testing support
- Custom checker support
- Time limit / Memory limit support
- Live progress in terminal

## Notes:
- Memory/Time usage will probably not be accurate, but personally I rarely benchmark my solution locally. If you REALLY want to track your memory/time usage accurately, I recommend you do custom testing on on whatever sites you are submitting (Codeforces, Atcoder, ...).
- Parallel testing is possible, but should not be overused, check your CPU usage and limit them accordingly (In my case 2-4 works best).
- [testlib](https://github.com/MikeMirzayanov/testlib) won't be used, since I find it way to overkill for my simple stress tester. Personally, I think [testlib](https://github.com/MikeMirzayanov/testlib) is better suited for online judges.

## How do I use it?
### Python
- This project uses [python](https://www.python.org/), install it if you haven't.
### Dependencies
- After that, navigate to the folder containing `requirements.txt`, open its terminal and install the necessary dependencies.
```bash
pip install -r requirements.txt
```
### Config setup
- Go to `config.py` and change some variables according to your setup. Here are some of the important ones:
  - `SOLUTION_PATH` - Path to your solution C++ file, defaulted at `src/sol.cpp` *(Note that `src/sol.cpp` is a **relative path**, if your C++ file is outside of the directory, use **full path** instead)*.
  - `BRUTE_PATH` - Path to your brute force C++ file, same as `SOLUTION_PATH`.
  - `SOLUTION_TIMELIMIT` - Time limit for your solution (in seconds).
  - `BRUTE_TIMELIMIT` - Time limit for your brute force (in seconds).
  - `MAX_TESTS` - The number of tests for your stress.
### Run
- Finally, just run the stress tester.
```bash
python stress.py
```

## Custom Checker
- Custom checker is supported, currently there is only one simple token implentation of the checker. If you want to add your own, make sure to follow this setup!
- **Path** to the output will be in `argv`, with `argv[1]` being the path to the solution output, and `argv[2]` being the brute force output path. So your code in `main()` should be something like this:
```cpp
int main(int argc, char *argv[]){
    ifstream sol(argv[1]);
    ifstream brute(argv[2]);
    (...)
}
```
- When returning, write into stdout to signal the stress that something has gone wrong. If not, then **do not** write into it, just exit normally! For example:
```cpp
int main(int argc, char *argv[]){
    (...)
    for (int i = 0; i < max(token1.size(), token2.size()); i++){
        if (i == token1.size()){
            cout << "Found unexpected EOL in participant";
            return 0;
        }
        if (i == token2.size()){
            cout << "Found unexpected token in participant";
            return 0;
        }
        if (token1[i] != token2[i]){
            cout << "Token " + to_string(i + 1) << " mismatch!";
            return 0;
        } 
    }
    return 0; // No problems detected
}
```
- Make sure to consider white spaces (like '\n') when comparing outputs, here is my `tokenize()` function, it takes in a stream, removing white spaces and return an array of tokens from it:
```cpp
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
```
