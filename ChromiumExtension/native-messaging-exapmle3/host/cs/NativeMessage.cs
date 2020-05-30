using System;
using System.IO;

namespace native2
{
    class NativeMessage
    {
        public static string OpenStandardStreamIn()
        {
            Stream stdin = Console.OpenStandardInput();
            int length = 0;
            byte[] bytes = new byte[4];
            stdin.Read(bytes, 0, 4);
            length = BitConverter.ToInt32(bytes, 0);
            string input = "";
            for (int i = 0; i < length; i++) input += (char)stdin.ReadByte();
            return input;
        }
        public static void OpenStandardStreamOut(string stringData)
        {
            string outString = "\"" + stringData + "\"";
            int dataLength = outString.Length;
            byte[] bytes = BitConverter.GetBytes(dataLength);
            Stream stdout = Console.OpenStandardOutput();
            for (int i = 0; i < 4; i++) stdout.WriteByte(bytes[i]);
            Console.Write(outString);            
        }
    }
}
