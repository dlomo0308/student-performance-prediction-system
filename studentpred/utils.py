from .models import Student

def generate_student_number():
    # prefix = 'A'  # Prefix for student numbers
    # starting_value = 2400  # Starting value for student numbers
    # random_suffix = random.randint(1000, 9999)  # Generate a random 4-digit number
    # student_id = f"{prefix}{starting_value + random_suffix}"  # Combine prefix and random suffix
    # return student_id
    last_student_id = Student.objects.last().student_id if Student.objects.exists() else 'A2399'
    prefix, last_number = last_student_id[:1], int(last_student_id[1:])
    new_number = last_number + 1
    new_student_id = f"{prefix}{new_number}"
    return new_student_id