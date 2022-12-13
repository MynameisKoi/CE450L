#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main(){
    int x[5];
    // set x[0] = 4500
    x[0] = 4500;
    for(int i=0; i<5; i++)
    {
        x[i] = i+1;
    }
    // print x
    cout << x << endl;
    cout << &x[0] << endl;
    cout << *x << endl;
    cout << x[1] << endl;
    cout << x[2] << endl;
    cout << &x[1] << endl;
}
