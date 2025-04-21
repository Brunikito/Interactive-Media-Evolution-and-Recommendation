#ifndef UNORDERED_LINKED_LIST_H
#define UNORDERED_LINKED_LIST_H
#include <cstdint>
#include <memory>
#include <iostream>
#include <vector>

namespace UnorderedLinkedList{

struct Node
{
    int64_t value;
    Node* nextNode;
    
    Node(int64_t val) : value(val), nextNode(nullptr) {}

};


class UnorderedLinkedList {
    public:
        Node* head;
        int64_t size;
        UnorderedLinkedList() : head(nullptr), size(0) {}

        void insert(int64_t value) {
            Node* newNode = new Node(value);
            newNode->nextNode = head;
            head = newNode;
            size++;
        }

        int64_t getSize() const { return size; }

        bool search(int64_t valueToSearch){
            Node* current = head;
            while (current){
                if (current->value == valueToSearch) return true;
                current = current->nextNode;
            }
            return false;
        }

        int64_t getNValue(int64_t N) {
            if (size == 0) throw std::out_of_range("List is empty");

            int64_t valueModSize = N % size;
            Node* current = head;
            for (int64_t i = 0; i < valueModSize; i++){
                current = current->nextNode;
            }
            return current->value;
        }
    
        ~UnorderedLinkedList() {
            Node* current = head;
            while (current != nullptr) {
                Node* next = current->nextNode;
                delete current;
                current = next;
            }
        }
};

}

#endif