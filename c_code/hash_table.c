#include "useful_functions.c"
#include "murmur3/murmur3.c"


#define HASHSIZE 104729

struct nlist {
    struct nlist *next;
    struct nlist *prev;
    int xkey;
    int ykey;
    unsigned char value;
};

typedef struct {
    struct nlist** HASHTABLE;
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
    tab->HASHTABLE = (struct nlist**)calloc(sizeof(struct nlist*),HASHSIZE);
}

unsigned char lookup(BoolTable* tab, int xkey, int ykey) {
    //printf("LOOK UP JAVERT!\n");
    struct nlist* np = tab->HASHTABLE[hash(xkey,ykey,tab->L)];
    if(np == NULL){
        return 0;
    }
    np = np->next;

    //printf("DID I DIE YET?\n");
    while(np->value!=2) {
        if(xkey==np->xkey && ykey == np->ykey) {
            return 1;
        }
        np = np->next;
    } return 0;
}

void install(BoolTable* tab, int xkey, int ykey) {
    //printf("INSTALLING\n");
    if(!lookup(tab, xkey,ykey)) {
        //printf("BITCHES\n");
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
        new_entry->next = current;
        new_entry->prev = current->prev;
        current->prev->next = new_entry;
        current->prev=new_entry; 
        //printf("OVER HEEEERREEEE\n");
        tab->HASHTABLE[hash(xkey,ykey,tab->L)] = current;
    }
}
void free_hash(BoolTable* tab) {
    struct nlist *np;
    struct nlist *next;
    for(int i=0; i<HASHSIZE;i++) {
        np = tab->HASHTABLE[i];
        if(np!=NULL) {
            np = np->next;
            while(np->value!=2) {
                next = np->next;
                free(np);
                np = next;
            }
            free(np);
        }
    }
    //printf("OUTSIDE\n");
    free(tab->HASHTABLE);
    free(tab);
}
