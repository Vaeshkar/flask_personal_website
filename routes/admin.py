from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes.auth import login_required
from db import get_connection
import base64

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin dashboard
@admin_bp.route('/')
@login_required
def admin():
   return render_template('admin/admin.html')

# Edit Profile (GET and POST)
@admin_bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
   # Handle POST (form submission)
   if request.method == 'POST':
      error = None
      data_uri = None
      full_name = request.form['full_name']
      bio = request.form['bio']
      location = request.form['location']
      email = request.form['email']
      picture = request.files['picture']

      if not full_name:
         error = 'Full name is required'
      elif not bio:
         error = 'Bio is required'
      elif not location:
         error = 'Location is required'
      elif not email:
         error = 'Email is required'

      if picture:
         allowed_extensions = ['image/jpeg', 'image/png', 'image/jpg']
         media_type = picture.mimetype
         if media_type not in allowed_extensions:
            error = 'Invalid file type. Please upload an image file'
         else:
            image_bytes = picture.read()
            if len(image_bytes) > 5000000:
               error = 'Image file is too large. Max size is 5MB'
            else:
               base64_data = base64.b64encode(image_bytes).decode('utf-8')
               data_uri = f"data:image/{media_type};base64,{base64_data}"

      if error is None:
         conn = get_connection()
         cur = conn.cursor()
         if data_uri is None:
            cur.execute(
               '''
               INSERT INTO personal_info (info_id, full_name, bio, location, email)
               VALUES (1, %s, %s, %s, %s)
               ON CONFLICT (info_id)
               DO UPDATE SET
                  full_name = EXCLUDED.full_name,
                  bio = EXCLUDED.bio,
                  location = EXCLUDED.location,
                  email = EXCLUDED.email
               ''',
               (full_name, bio, location, email)
            )
         else:
            cur.execute(
               '''
               INSERT INTO personal_info (info_id, full_name, bio, location, email, picture)
               VALUES (1, %s, %s, %s, %s, %s)
               ON CONFLICT (info_id)
               DO UPDATE SET
                  full_name = EXCLUDED.full_name,
                  bio = EXCLUDED.bio,
                  location = EXCLUDED.location,
                  email = EXCLUDED.email,
                  picture = EXCLUDED.picture
               ''',
               (full_name, bio, location, email, data_uri)
            )
         conn.commit()
         cur.close()
         conn.close()
         return redirect(url_for('admin.edit_profile'))
      else:
         flash(error)

   # Handle GET request for displaying the form
   conn = get_connection()
   cur = conn.cursor()
   cur.execute("SELECT * FROM personal_info")
   personal_info = cur.fetchone()
   cur.close()
   conn.close()

   data = {
      'full_name': personal_info[1] if personal_info else '',
      'bio': personal_info[2] if personal_info else '',
      'location': personal_info[3] if personal_info else '',
      'email': personal_info[4] if personal_info else '',
      'picture': personal_info[5] if personal_info else ''
   }

   return render_template('admin/edit-profile.html', data=data)

# Edit Projects (View and Edit)
@admin_bp.route('/edit-projects')
@login_required
def edit_projects():
   conn = get_connection()
   cur = conn.cursor()
   cur.execute("SELECT * FROM projects")
   result_from_projects = cur.fetchall()
   cur.close()
   conn.close()

   projects = []
   for project in result_from_projects:
      projects.append({
         'id': project[0],
         'name': project[1],
         'demo_url': project[2],
         'image': project[3],
         'description': project[4]
      })
   return render_template('admin/edit-projects.html', projects=projects)

# Delete Project
@admin_bp.route('/delete-project/<int:id>', methods=['POST'])
@login_required
def delete_project(id):
   conn = get_connection()
   cur = conn.cursor()
   cur.execute("DELETE FROM projects WHERE project_id = %s", (id,))
   conn.commit()
   cur.close()
   conn.close()
   return redirect(url_for('admin.edit_projects'))

# Edit Individual Project (GET and POST)
@admin_bp.route('/edit-project/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    if request.method == 'POST':
        error = None
        name = request.form['name']
        demo_url = request.form['demo_url']
        description = request.form['description']
        image = request.files['image']
        data_uri = None

        if not name:
            error = 'Project name is required'
        elif not demo_url:
            error = 'Demo URL is required'
        elif not description:
            error = 'Description is required'

        if image:
            allowed_extensions = ['image/jpeg', 'image/png', 'image/jpg']
            media_type = image.mimetype
            if media_type not in allowed_extensions:
                error = 'Invalid file type. Please upload an image file.'
            else:
                image_bytes = image.read()
                if len(image_bytes) > 5000000:
                    error = 'Image file is too large. Max size is 5MB.'
                else:
                    base64_data = base64.b64encode(image_bytes).decode('utf-8')
                    data_uri = f"data:image/{media_type};base64,{base64_data}"

        if error is None:
            conn = get_connection()
            cur = conn.cursor()

            # If an image was provided, update the image as well
            if data_uri:
                cur.execute('''
                    UPDATE projects
                    SET project_name = %s, demo_url = %s, description = %s, image = %s
                    WHERE project_id = %s
                ''', (name, demo_url, description, data_uri, id))
            else:
                cur.execute('''
                    UPDATE projects
                    SET project_name = %s, demo_url = %s, description = %s
                    WHERE project_id = %s
                ''', (name, demo_url, description, id))

            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('admin.edit_projects'))
        else:
            flash(error)

    # Handle GET request for editing a project
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects WHERE project_id = %s", (id,))
    project = cur.fetchone()
    cur.close()
    conn.close()

    if project is None:
        return render_template('404.html'), 404

    data = {
        'id': project[0],
        'name': project[1],
        'demo_url': project[2],
        'image': project[3],
        'description': project[4]
    }

    return render_template('admin/edit-project.html', data=data)

# ADD project – (GET and POST)
@admin_bp.route('/add-project', methods=['GET', 'POST'])
@login_required
def add_project():
   if request.method == 'POST':
      error = None
      data_uri = None
      name = request.form['name']
      demo_url = request.form['demo_url']
      description = request.form['description']
      image = request.files['image']
      if(not name):
         error = 'Project name is required'
      elif(not demo_url):
         error = 'Demo URL is required'
      elif(not description):
         error = 'Description is required'
 
      if image:
         allowed_extensions = ['image/jpeg', 'image/png', 'image/jpg']
         media_type = image.mimetype
         if(media_type not in allowed_extensions):
            error = 'Invalid file type. Please upload an image file'
         else:
            image_bytes = image.read()
            if(len(image_bytes) > 5000000):
               error = 'Image file is too large. Max size is 5MB'
            else:
               base64_data = base64.b64encode(image_bytes).decode('utf-8')
               data_uri = f"data:image/{media_type};base64,{base64_data}"
 
      if error is None:
         conn = get_connection()
         cur = conn.cursor()
         cur.execute(
            '''
            INSERT INTO projects (project_name, demo_url, image, description)
            VALUES (%s, %s, %s, %s)
            ''',
            (name, demo_url, data_uri, description)
         )
         conn.commit()
         cur.close()
         conn.close()
         return redirect(url_for('admin.edit_projects'))
      else:
         flash(error)
         return redirect(url_for('admin.add_project'))
   return render_template('admin/add-project.html')