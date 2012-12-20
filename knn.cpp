#include<fstream>
#include<cstring>
#include<boost/algorithm/string.hpp>
#include<vector>
#include<iostream>


int main(int argc, char** argv)
{
	std::ifstream infile("train.csv");

	int i = 0;
	
	while( i < 1000)
	{
		std::string s;
		infile >> s;
		std::vector<std::string> strs;
		boost::split(strs , s , boost::is_any_of(","));
		i++;
	}

	infile.close();
}

