using System;

namespace native2
{
    class Program
    {
        static void Main(string[] args)
        {
          for(int i=0; i<5; i++) {
            string outString = "host.exe start";
            NativeMessage.OpenStandardStreamOut(outString);
            string inStr = NativeMessage.OpenStandardStreamIn();
            //NativeMessage.OpenStandardStreamOut("received message");
            //NativeMessage.OpenStandardStreamOut("{\"text\":\"aaa\"}");
            NativeMessage.OpenStandardStreamOut(inStr.Substring(10,3));
            //Console.WriteLine(inStr);
          }
        }
    }
}
