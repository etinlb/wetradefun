
def sort(unsorted_list, sort_field, asc_or_desc):
    """ Sorts a semi-sorted list in place. The initial list must be one list
    appended to another, each must be in DESCENDING order. Sort occurs in
    place so original list is modified.
    
    unsorted_list - a list made of 2 lists (one appending another), each
        sorted in DESCENDING order by the sort_field attribute of each element
    sort_field - attribute of each element to sort the entire list by
        (each element must have this attribute)
    asc_or_desc - result wanted in ascending or descending order?
        must be either "asc" or "desc"

    """    

    h = unsorted_list

    a = 0 # counter for 1st inner list
    while (a+1 < len(h)):
        if (getattr(h[a+1], sort_field) > getattr(h[a], sort_field)):
            b = a+1 # counter for 2nd inner list
            break
        else:
            a+=1

    # sort descending
    a = 0
    try:
        while (a < b):
            if (getattr(h[b], sort_field) > getattr(h[a], sort_field)):
                h.insert(a, h[b])
                del(h[b+1])
                
                if (b+1 < len(h)):
                    b+=1
                else:
                    break
            else:
                a+=1
    except UnboundLocalError:
        pass # list already sorted!

    # if want asc, reverse list
    if (asc_or_desc == "asc"):
        h.reverse()
    elif (asc_or_desc != "desc"):
        raise NotImplementedError, "'" + asc_or_desc + "' must either be 'asc' or 'desc'"
