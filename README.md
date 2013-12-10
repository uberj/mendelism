Exploring Meiosis and Mendel's genetics.
----------------------------------------

This is a dead simple simulator used for experimenting with what happens when
you self cross a simple cell with itself. This work was inspired by the basic
explanation of genetics given in my biology text book.


Terms
-----
* A trait is represented by a letter
* An allele is either the upper or lower case of a letter. Together two alleles make up a gene
* A chromosome is a string of alleles
* Initially, every chromosome must have another chromosome of equal length

See `mendelism/cell.py` for a full listing of terms from the textbook.

Examples
--------
A mono hybrid self cross with one heterozygous gene.
```
uberj $> python simulate.py X x
Gamete Results
--------------
X:   0.5
x:   0.5

F2 Results
-----------
XX:   0.2483
Xx:   0.5018
xx:   0.2499

Aggregate Probabilities
-----------------------
xx:    0.2499
XX:    0.2483
Xx:    0.5018
Sum of aggregate probabilities: 1.0
```

A dihybrid self cross of a cell heterozygous for both seed color and seed shape. 100000 simulated breedings were done.
```
uberj $> python simulate.py --num-trials 100000 YR yr
Gamete Results
--------------
YR:   0.37560125
Yr:   0.12439875
yR:   0.12439875
yr:   0.37560125

F2 Results
-----------
RR:   0.24899
Rr:   0.50206
YY:   0.24943
Yy:   0.5004
rr:   0.24895
yy:   0.25017

Aggregate Probabilities
-----------------------
yyrr:    0.0622798215
yyRR:    0.0622898283
yyRr:    0.1256003502
Yyrr:    0.12457458
YyRR:    0.124594596
YyRr:    0.251230824
YYrr:    0.0620955985
YYRR:    0.0621055757
YYRr:    0.1252288258
Sum of aggregate probabilities: 1.0
```

An example of simulating a cell with different length chromosomes. The cell
was: heterozygous for seed color, seed shape, and flower position; homozygous
dominant for pod color; homozygous recessive for stem length.
```
uberj $> python simulate.py YR yr Gat GAt
Gamete Results
--------------
YARtG:   0.1861
YArtG:   0.0638375
YaRtG:   0.188775
YartG:   0.0612875
yARtG:   0.0613625
yArtG:   0.1887
yaRtG:   0.0637625
yartG:   0.186175

F2 Results
-----------
AA:   0.2525
Aa:   0.5014
GG:   1.0
RR:   0.2531
Rr:   0.4988
YY:   0.2532
Yy:   0.4997
aa:   0.2461
rr:   0.2481
tt:   1.0
yy:   0.2471

Aggregate Probabilities
-----------------------
aaYYttGGRr:    0.031081484976
aaYYttGGRR:    0.015771298812
aaYYttGGrr:    0.015459736212
aaYyttGGRr:    0.061340513596
aaYyttGGRR:    0.031125268627
aaYyttGGrr:    0.030510387777
aayyttGGRr:    0.030332681428
aayyttGGRR:    0.015391342561
aayyttGGrr:    0.015087286011
AAYYttGGRr:    0.0318897804
AAYYttGGRR:    0.0161814423
AAYYttGGrr:    0.0158617773
AAYyttGGRr:    0.0629357159
AAYyttGGRR:    0.031934702675
AAYyttGGrr:    0.031303831425
AAyyttGGRr:    0.0311215037
AAyyttGGRR:    0.015791605025
AAyyttGGrr:    0.015479641275
AaYYttGGRr:    0.063324894624
AaYYttGGRR:    0.032132178888
AaYYttGGrr:    0.031497406488
AaYyttGGRr:    0.124974130504
AaYyttGGRR:    0.063414098698
AaYyttGGrr:    0.062161350798
AayyttGGRr:    0.061799294872
AayyttGGRR:    0.031358062414
AayyttGGrr:    0.030738582714
Sum of aggregate probabilities: 1.0
```

