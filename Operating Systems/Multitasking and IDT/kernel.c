#include <stdint.h>
void k_clearscr();
void run_test();
void dispatch_leave();
void dispatch();
void go();
void p1();
void p2();
void k_printstr(char *string, int row, int col);
void print_border(int start_row, int start_col, int end_row, int end_col);
int create_process(uint32_t code_address);
int totalvar;
int next_pid = 0;
struct pcbq_t {
pcb_t *front;
pcb_t *end;
}typedef pcbq_t pcbq_t;
struct pcb_t {
pcb_t *next;
pcb_t *junk;
uint32_t esp;
uint32_t pid;
}typedef pcb_t pcb_t;
pcbq_t *RunningQueue;
pcb_t *Running;
void enqueue(pcbq_t *q, pcb_t *pcb);
pcb_t *dequeue(pcbq_t *q);
struct idt_entry{
    uint16_t base_low;
    uint16_t selector;
    uint8_t always0;
    uint8_t access;
    uint16_t base_hi;
    }__attribute__((packed)) typedef struct idt_entry idt_entry_t;
idt_entry_t idt[256];
idt_entry_t *entry;
void init_idt_entry(idt_entry_t *entry, uint32_t addr_of_handler, uint16_t selector, uint8_t access);
void init_idt();
struct idtr{
    uint16_t limit;
    uint32_t base;}__attribute__((packed)) typedef idtr idtr;
void lidtr(idtr *idtr);
void print_return();
int main()  
{
    uint32_t code_address1 = (uint32_t) p1;
    uint32_t code_address2 = (uint32_t) p2;
    run_test();
    k_clearscr();
    print_border(0, 0, 24, 79);
    RunningQueue = kmalloc(sizeof(pcbq_t));
    Running = kmalloc(sizeof(pcb_t));
    k_printstr("Running Processes....", 1, 1);
    init_idt();
    int process_return1 = create_process(code_address1);
    int process_return2 = create_process(code_address2);
    go();
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
                if(i == 0 && j == 0 || i ==0 && j == 79 || i == 24 && j == 79 || i == 24 && j== 0 || i == 10 && j == 10 || i == 15 && j == 10 || i == 10 && j == 35 || i == 13 && j == 35 || i == 13 && j == 10 || i == 15 && j == 35 || i == 18 && j == 35 || i == 18 && j == 10){
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
int create_process(uint32_t code_address){
    uint32_t size = 1024;
    uint32_t* stackptr = kmalloc(size);                
    uint32_t* st = stackptr + 1024;                   
    st--;
    *st = 0;                                           
    st--;
    *st = 16;                                          
    st--;
    *st = code_address;                                
    st--;
    *st = (uint32_t) dispatch_leave;                               
    for (int i=0; i<8; i++){
        st--;
        *st = 0;

    }
    pcb_t *pcb = kmalloc(96);
    pcb->esp = (uint32_t)st;
    pcb->pid = next_pid;
    next_pid++;
    enqueue(RunningQueue, pcb);
    return 0;
}
void p1(){
print_border(10, 10, 13, 35);
k_printstr("Process 1 running...", 11, 11);
int num = 0;
char Charnum[20];
int s;
k_printstr("Value: ", 12, 11);
while(1==1){
    convert_num(num, Charnum);
    k_printstr(Charnum, 12, 18);
    num++;
    if(num > 999){
        num = 0;      
    }
    asm("int $32");
}}
void p2(){
print_border(15, 10, 18, 35);
k_printstr("Process 2 running...", 16, 11);
int num = 0;
char Charnum[20];
int s;
k_printstr("Value: ", 17, 11);
while(1==1){
     convert_num(num, Charnum);
    k_printstr(Charnum, 17, 18);
    num++;
    if(num > 999){
        num = 0;
        
            
    }
    asm("int $32");
}
}
void enqueue(pcbq_t *q, pcb_t *pcb){
    if(q->front == 0){
        q->front = pcb;
        q->end = pcb;
        totalvar++;
    }else{
        q->end->next = pcb;
        q->end = pcb;
        totalvar++;
    }
}
pcb_t *dequeue(pcbq_t *q){
    if(q->front == 0){
        return 0;
    }else{
        pcb_t *pcb = q->front;
        q->front = q->front->next;
        totalvar--;
        if(totalvar == 1){
            q->end = q->front;
        }
        return pcb;
    }
}

 void init_idt_entry(idt_entry_t *entry, uint32_t addr_of_handler, uint16_t code_selector, uint8_t access){
    entry->base_low = (uint16_t)addr_of_handler & 0xFFFF;
    entry->base_hi = (uint16_t)(addr_of_handler >> 16) & 0xFFFF;
    entry->selector = code_selector;
    entry->always0 = 0;
    entry->access = access;
}

void init_idt(){
    for (int i=0; i<255; i++){
        if(i<32){
            init_idt_entry(&idt[i], (uint32_t) print_return, 16, 0x8E);
        }
        else if(i==32){
            init_idt_entry(&idt[i], (uint32_t) dispatch, 16, 0x8E);
        }
        else{
            init_idt_entry(&idt[i],0,0,0);
        }
    }

    idtr idtr;
    idtr.limit = sizeof(idt_entry_t)*256 - 1;
    idtr.base = (uint32_t)idt;
    lidtr(&idtr);
}

void print_return(){
    k_printstr("Error", 1, 1);
}