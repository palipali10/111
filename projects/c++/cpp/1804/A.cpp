#include <iostream>
#include <vector>
using namespace std;


void solv(){
    int n; 
    vector<int> v; 

    for(int x=0; x<n; x++){
        cin >> v[x];
    }

    for(int x=0; x<v.size(); x++){
        cout << v[x] << endl;
    }

}

int main(){
    int t; cin >> t;
    while(t--){
        solv();
    }

    return 0;
}




































