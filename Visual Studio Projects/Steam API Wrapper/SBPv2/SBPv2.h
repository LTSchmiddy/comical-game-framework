// The following ifdef block is the standard way of creating macros which make exporting 
// from a DLL simpler. All files within this DLL are compiled with the SBPV2_EXPORTS
// symbol defined on the command line. This symbol should not be defined on any project
// that uses this DLL. This way any other project whose source files include this file see 
// SBPV2_API functions as being imported from a DLL, whereas this DLL sees symbols
// defined with this macro as being exported.
#ifdef SBPV2_EXPORTS
#define SBPV2_API __declspec(dllexport)
#else
#define SBPV2_API __declspec(dllimport)
#endif

// This class is exported from the SBPv2.dll
class SBPV2_API CSBPv2 {
public:
	CSBPv2(void);
	// TODO: add your methods here.
};

extern SBPV2_API int nSBPv2;

SBPV2_API int fnSBPv2(void);
