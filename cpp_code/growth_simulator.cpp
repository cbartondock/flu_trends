#include <fstream>
#include <iostream>
#include <string>
#include <cstdlib>
#include <cmath>
using namespace std;

int main() {

    ifstream inf("flu_data.csv");
    if(!inf)
    {
        cerr << "Could not be opened for reading!" << endl;
        exit(1);
    }

    while(inf) 
    {
        std::string strInput;
        inf >> strInput;
        cout << strInput << endl;
    }

    return 0;
}
