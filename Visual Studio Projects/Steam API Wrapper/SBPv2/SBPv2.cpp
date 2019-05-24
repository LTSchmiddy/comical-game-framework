

#include "stdafx.h"
#include "SBPv2.h"
#include <iostream>
#include <string>
//#include "Python.h"
#include "steam\\public\\steam\\steam_api.h"

#ifdef _DEBUG
#undef _DEBUG
#include <Python.h>
#define _DEBUG
#else
#include <Python.h>
#endif



// SBPv2.cpp : Defines the exported functions for the DLL application.
// This is an example of an exported variable
SBPV2_API int iSBPv2 = 0;




// This is an example of an exported function.
SBPV2_API int initSteam_Wrap(void)
{	
	int retVal = SteamAPI_Init();
	std::cout << retVal << "\n";
	//exit(0);
    return retVal;
	
}

// This is the constructor of a class that has been exported.
// see SBPv2.h for the class definition


extern "C" {

	SBPV2_API int nSBPv2 = iSBPv2;
	SBPV2_API int initSteam() {
		return initSteam_Wrap(); 
	}

	SBPV2_API char * spam_system(void) {
		return "Steam DLL Loaded!! HUZZAH!!";
	}
}