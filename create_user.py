from django.contrib.auth.models import User

# Check if the user exists
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'root_0987')
    print("Created admin user")
else:
    # Update password if it exists just in case
    u = User.objects.get(username='admin')
    u.set_password('root_0987')
    u.save()
    print("Updated admin password")
