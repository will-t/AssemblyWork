void k_clearscr();
void run_test();
void k_printstr(char *string, int row, int col);
void print_border(int start_row, int start_col, int end_row, int end_col);
int res1;
int res2;
int res3;
int res4;

int main()  
{
    res1 =0;
    res2 =0;
    res3 =24;
    res4 =79;
    k_clearscr();
    print_border(res1, res2, res3, res4);
    run_test();
    int z = 0;
    for(z=0;;){

    }
    return 0;
}

void k_clearscr()  
{
    int i;
    for (i = 0; i < 25; i++)  
    {
        k_printstr("                                                                                ", i, 0);
    }
}
void print_border(int start_row, int start_col, int end_row, int end_col){
    int i;
    int j;
    for (i = start_row; i <= end_row; i++){
        for (j = start_col; j <= end_col; j++){
            if (i == start_row || i == end_row){
                if(i == 0 && j == 0 || i ==0 && j == 79 || i == 24 && j == 79){
                    k_printstr("+", i, j);
                   
                }else{
                    k_printstr("-", i, j);
                }
                
            }
            else if (j == start_col || j == end_col){
                k_printstr("|", i, j);
            }
        }
    }
}