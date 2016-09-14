def sortStack(stack):
    tmpStack = []
    pivot = stack[-1]
    swap_count = len(stack)
    forward = True
    while(swap_count > 0):
        counter = 0
        if forward:
            pivot = stack[-1]
        else:
            pivot = tmpStack[-1]
        while(counter < swap_counter):
            if forward:
                item = stack.pop()
                if item > pivot:
                    tmpStack.append(pivot)
                    pivot = item
                else:
                    tmpStack.append(item)
            else:
                item = tmpStack.pop()
                if item 
            counter += 1
        swap_count -= 1
        forward = not forward
