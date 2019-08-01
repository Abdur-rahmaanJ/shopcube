using System.Diagnostics;
using System.IO;

namespace SilentCommand
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            Process process = new Process();
			
	    // [Optional]Sets  workind directory executable current directory
            process.StartInfo.WorkingDirectory = Directory.GetCurrentDirectory();
			
            process.StartInfo.WindowStyle = ProcessWindowStyle.Hidden;

	    // Name|path of process|executable to start
            process.StartInfo.FileName = "python";
			
	    // [Optional] Arguments
            process.StartInfo.Arguments = "app.py";

            process.Start();
			
	    // [Optional] Open specific URL in  Browser
	    // Process.Start("http://127.0.0.1:5000");

        }
    }
}