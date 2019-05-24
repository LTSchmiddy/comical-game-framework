using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;

namespace Comical_Launcher_v1_cs
{
    class Program
    {
        public static bool usePythonCommandLine = false;
        public static bool useUncompiledFile = false;

        static void Main(string[] args)
        {
            if (args.Contains("--usePythonCommandLine")) {
                usePythonCommandLine = true;
            }

            if (args.Contains("--useUncompiledFile"))
            {
                usePythonCommandLine = true;
            }

            LaunchCommandLineApp();
        }

        /// <summary>
        /// Launch the legacy application with some options set.
        /// </summary>
        static void LaunchCommandLineApp()
        {
            // For the example
            //const string ex1 = "C:\\";
            //const string ex2 = "C:\\Dir";

            // Use ProcessStartInfo class
            ProcessStartInfo startInfo = new ProcessStartInfo();
            startInfo.CreateNoWindow = false;
            startInfo.UseShellExecute = false;
            startInfo.FileName = "python27/pythonw.exe";
            if (usePythonCommandLine)
            {
                startInfo.FileName = "python27/python.exe";
            }
            
            startInfo.WindowStyle = ProcessWindowStyle.Hidden;
            startInfo.Arguments = "Disp_Host.pyc";

            if (useUncompiledFile)
            {
                startInfo.Arguments = "Disp_Host.py";
            }


            //try
            //{
            // Start the process with the info we specified.
            // Call WaitForExit and then the using statement will close.
            using (Process exeProcess = Process.Start(startInfo))
            {
                exeProcess.WaitForExit();
            }
            //}
            //catch
            //{
            //    // Log error.
            //}
        }
    }
}