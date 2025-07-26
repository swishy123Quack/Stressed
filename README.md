# Stressed
A competitive programming stress tester

WARNING: Mac/Unix support is NOT supported! Only run this on Windows.

Features:
- Customizable
- Setting time limit
- Parallel test
- Progress tracking in terminal

Notes:
- Memory limiting is technically possible, but this is rather a pain to setup on Windows (easier on Unix platform). Besides, if your program eats 1GB of memory, you are probably doing something wrong. If you REALLY want to track your memory/time usage accurately, I recommend you do custom testing on on whatever sites you are submitting (Codeforces, Atcoder, ...)
- Parallel testing is possible, but should not be overused, check your CPU cores before setting the limits (In my case 2-4 works best)
