clear
cd "C:\MySpace\GitHub\BUS-Z-798\PyforDataSimulation"
use data.dta, clear


**************Part 1**************

*icc
icc Construct1 Person
icc Construct1 Time

icc Construct2 Person
icc Construct2 Time

icc Construct3 Person
icc Construct3 Time

*ira
ira Person Construct1 group(Time)
ira Time Construct1 group(Person)

ira Person Construct2 group(Time)
ira Time Construct2 group(Person)

ira Person Construct3 group(Time)
ira Time Construct3 group(Person)

*null model
twoway connected Construct1 Time if Person!=-1, connect(L) //用if暗示id变量，就能画在一张图上
twoway connected Construct1 Time, by(Person) connect(L) //直接group id,就是画多张图
twoway connected Construct1 Time, connect(L) // 什么都不加，似乎也可以

mixed Construct1 || Person:
estat icc

mixed Construct2 || Person:
estat icc

mixed Construct3 || Person:
estat icc


**************Part 2**************
use "multilevel exercise.dta", clear

* ICC
icc transformational teamid
icc engagement teamid

* rwg
sum transformational
tabulate transformational

egen sd_trans = sd(transformational), by(teamid)
gen S2_trans = sd_trans^2
drop sd_trans

egen sd_enga = sd(engagement), by(teamid)
gen S2_enga = sd_enga^2
drop sd_enga

gen RwgU= 1- S2_enga/4
recode RwgU (-1e+10/0=0)

gen RwgS= 1- S2_enga/2.9
recode RwgS (-1e+10/0=0)

sum RwgU RwgS

******** Prepare Data
egen trans = mean(transformational), by(teamid)
gen consci = conscientiousness
egen consci_gm = mean(consci), by(teamid)
gen consci_gmc = consci - consci_gm

******** Uncenterd Data
*Null model
mixed engagement || teamid:
estat icc
estadd scalar icc = r(icc2)
estimates store Model1

*Random coefficient model
mixed engagement consci || teamid: consci, covariance(unstructured) nolog
estat icc
estadd scalar icc = r(icc2)
estimates store Model2

*Intercepts as outcomes model
mixed engagement consci trans || teamid: , cov(un)
estat icc
estadd scalar icc = r(icc2)
estimates store Model3

*Slopes as outcomes model
mixed engagement c.consci##c.trans|| teamid: consci, cov(un)
estat icc
estadd scalar icc = r(icc2)
estimates store Model4

******** Centerd Data
*Null model
mixed engagement || teamid:


*Random coefficient model
mixed engagement consci_gmc || teamid: consci_gmc, stddev covariance(unstructured) nolog
estat icc
estadd scalar icc = r(icc2)
estimates store Model5

*Intercepts as outcomes model
mixed engagement consci_gmc trans || teamid: , cov(un)
estat icc
estadd scalar icc = r(icc2)
estimates store Model6

*Slopes as outcomes model
mixed engagement c.consci_gmc##c.trans|| teamid: consci_gmc, cov(un)
estat icc
estadd scalar icc = r(icc2)
estimates store Model7

*Slopes as outcomes model
mixed engagement consci_gm c.consci_gmc##c.trans|| teamid: consci_gmc, cov(un)
estat icc
estadd scalar icc = r(icc2)
estimates store Model8

* ssc install estout
esttab Model1 Model2 Model3 Model4 Model5 Model6 Model7 Model8, se aic bic scalars(icc ll df_m) ///
 transform(ln*: exp(@)^2 exp(@)^2) ///
 eqlabels(“” “var(Constant)” “var(Residual)” ), ///
 using Chapter4_table1.html, replace
