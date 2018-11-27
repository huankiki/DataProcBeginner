#!/bin/bash

python eval.py ref.out str.out str_wer.out test_v3.txt > ./rst/str_wer
python eval.py ref.out str.out spell.out test_v3.txt > ./rst/spell
python eval.py ref.out str.out spell_wer.out test_v3.txt > ./rst/spell_wer
python eval.py ref.out str.out str_spell_wer.out test_v3.txt > ./rst/str_spell_wer
python eval.py ref.out str.out str_spell.out test_v3.txt > ./rst/str_spell
python eval.py ref.out str_wer.out spell_wer.out test_v3.txt > ./str_wer_comp_spell_wer
