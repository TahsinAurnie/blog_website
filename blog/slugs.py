import random
import string
from django.utils.text import slugify

def generate_unique_slug(instance, base_title, new_slug=False, update=False): # instance has the class of the obj created
    slug = slugify(base_title)
    model = instance.__class__             # Blog class/model
    if new_slug:
        slug = new_slug

    if update:                             # if any blog related obj is updated
        slug_exists = model.objects.filter(    
        slug__icontains = slug             
    ).exclude(pk=instance.pk)              # exclude that blog id if any other entry with that slug of title exists
    else:
        slug_exists = model.objects.filter(    
        slug__icontains = slug             # checking if the slug already exists
    ).exists()
        
    if slug_exists:
        random_str = "".join(random.choices(string.ascii_lowercase, k=4)) # convert from 4 length list to string of len 4
        new = slugify(base_title + '-' + random_str)
        return generate_unique_slug(instance, base_title, new_slug = new)
    

    return slug
