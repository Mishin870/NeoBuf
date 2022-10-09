"""
Module for generating empty NeoBuf class templates
"""


def make_template():
    return f"""// This file was generated via NeoBuf. Please, do not modify manually
// Этот файл был сгенерирован через NeoBuf. Пожалуйста, не редактируйте его вручную
// https://github.com/Mishin870/NeoBuf

%usings%

namespace %package% [
    public class %name% : Message [
%variables%

        public override void Read(DataStream Data) [
%read%
        ]

        public override void Write(DataStream Data) [
%write%
        ]
    ]
]
    """.replace("[", "{").replace("]", "}")
