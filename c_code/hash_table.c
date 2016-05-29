#include "useful_functions.c"
#include "murmur3/murmur3.c"


#define HASHSIZE 1020379

struct nlist {
    struct nlist *next;
    struct nlist *prev;
    int xkey;
    int ykey;
    unsigned char value;
};

typedef struct {
    struct nlist* HASHTABLE[HASHSIZE];
    int L;
} BoolTable;



unsigned int hash(int xkey, int ykey, int L) {
    int index = (L+xkey) + (L+ykey)*L;
    uint32_t* hashval=(uint32_t*)malloc(sizeof(uint32_t));
    MurmurHash3_x86_128(&index, sizeof(int), 42, hashval);
    unsigned int result =  ((unsigned int)(*hashval))%HASHSIZE;
    return result;
}

void init_h(BoolTable *tab, int L) {
    tab->L = L;
}

unsigned char lookup(BoolTable* tab, int xkey, int ykey) {
    struct nlist* np = tab->HASHTABLE[hash(xkey,ykey,tab->L)];
    if(np == NULL){
        return 0;
    }
    np = np->next;
    while(np->value!=2) {
        if(xkey==np->xkey && ykey == np->ykey) {
            return 1;
        }
        np = np->next;
    } return 0;
}

void install(BoolTable* tab, int xkey, int ykey) {
    if(!lookup(tab, xkey,ykey)) {
        struct nlist* new_entry = (struct nlist*)malloc(sizeof(struct nlist));
        new_entry->xkey = xkey;
        new_entry->ykey = ykey;
        new_entry->value = 1; 
        struct nlist* current = tab->HASHTABLE[hash(xkey, ykey, tab->L)];
        if(current==NULL) {
            current = (struct nlist*)malloc(sizeof(struct nlist));
            current->prev = current;
            current->next = current;
            current->value = 2; //SENTINEL
        } 
        struct nlist* prev = current->prev;
        prev->next = new_entry;
        current->prev = new_entry;
        new_entry->prev = prev;
        new_entry->next = current;
        tab->HASHTABLE[hash(xkey,ykey,tab->L)] = current;
    }
}
