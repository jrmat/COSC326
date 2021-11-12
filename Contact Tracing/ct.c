/* Use "gcc -O2 -o ct ct.c" to compile the code;
** Then use "./ct 1000 10000 1000000000" to create a
** billion records for testing. 
** Warning: It can take 12GB disk space */

# include <stdio.h>
# include <stdlib.h>
# include <time.h>
# include <string.h>

int *trace;

int main(int argc, char * argv[]) {
  int c, i, n, m, k, maxn, maxm, maxk;
  if(argc != 4) {
	printf("Usage: %s <ID_range> <Time_range> <#records>\n", argv[0]);
	exit(0);
  }
  maxn = atoi(argv[1]);
  maxm = atoi(argv[2]);
  maxk = atoi(argv[3]);
  
  srand(time(NULL));

  for (c = 0; c < maxk; c++) {
    n = rand() % maxn + 1;
    m = rand() % maxn + 1;
    k = rand() % maxm + 1;
    if (n != m) {
      printf("%d %d %d\n", n, m, k);
    }
  }    
}      

