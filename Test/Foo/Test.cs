// This file was generated via NeoBuf. Please, do not modify manually
// Этот файл был сгенерирован через NeoBuf. Пожалуйста, не редактируйте его вручную
// https://github.com/Mishin870/NeoBuf

using System.Collections.Generic;
using NeoSeusCore.Messages;
using NeoSeusCore.Network.Transport;
using SomeNamespace.SomeClass;
using SomeNamespace.SomeEnum;

namespace Test.Foo {
    public class Test : Message {
        public int Color;
        public string Name;// Some inline comment
        
        // Some comment for Aliases (used only at variable definition and makes empty line at networking code)
        public List<string> Aliases;
        
        public SomeEnum MyEnum;
        public SomeClass MyClass;
        public List<SomeClass> ListOfMyClasses;

        public override void Read(DataStream Data) {
            Color = Data.ReadInt();
            Name = Data.ReadString();
            
            Aliases = Data.ReadList(NetworkHelper.STRING_READER);
            
            MyEnum = (SomeEnum)Data.ReadInt();
            MyClass = SomeClass.READER(Data);
            ListOfMyClasses = Data.ReadList(SomeClass.READER);
        }

        public override void Write(DataStream Data) {
            Data.WriteInt(Color);
            Data.WriteString(Name);
            
            Data.WriteList(Aliases, NetworkHelper.STRING_WRITER);
            
            Data.WriteInt((int) MyEnum);
            SomeClass.WRITER(Data, MyClass);
            Data.WriteList(ListOfMyClasses, SomeClass.WRITER);
        }
    }
}
    