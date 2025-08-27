#!/usr/bin/env python3
"""
Initialize demo data for SIAKAD
This script will create sample students, teachers, and classes
"""

from app import app, db, User, Student, Teacher, SchoolClass, Subject
from werkzeug.security import generate_password_hash
from datetime import datetime, date

def init_demo_data():
    """Initialize the database with demo data"""
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Clear existing data (for demo purposes)
        db.session.query(Student).delete()
        db.session.query(Teacher).delete()
        db.session.query(SchoolClass).delete()
        db.session.query(Subject).delete()
        
        # Keep admin user but clear others
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@siakad.com',
                password_hash=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
        
        # Create sample teachers
        teachers_data = [
            {
                'nip': '198501012010012001',
                'name': 'Dr. Sari Widodo, M.Pd',
                'email': 'sari.widodo@sekolah.ac.id',
                'phone': '081234567890',
                'address': 'Jl. Pendidikan No. 123, Jakarta Selatan',
                'subject': 'Matematika'
            },
            {
                'nip': '198203152009021002',
                'name': 'Ahmad Sutanto, S.Pd',
                'email': 'ahmad.sutanto@sekolah.ac.id',
                'phone': '081234567891',
                'address': 'Jl. Guru No. 456, Jakarta Timur',
                'subject': 'Bahasa Indonesia'
            },
            {
                'nip': '198712052011012003',
                'name': 'Rina Melati, S.S, M.Pd',
                'email': 'rina.melati@sekolah.ac.id',
                'phone': '081234567892',
                'address': 'Jl. Sastra No. 789, Jakarta Barat',
                'subject': 'Bahasa Inggris'
            },
            {
                'nip': '198406201010012004',
                'name': 'Budi Santoso, S.Si',
                'email': 'budi.santoso@sekolah.ac.id',
                'phone': '081234567893',
                'address': 'Jl. Sains No. 321, Jakarta Utara',
                'subject': 'Fisika'
            },
            {
                'nip': '198809131012012005',
                'name': 'Dewi Sartika, S.Pd',
                'email': 'dewi.sartika@sekolah.ac.id',
                'phone': '081234567894',
                'address': 'Jl. Sejarah No. 654, Jakarta Pusat',
                'subject': 'Sejarah'
            },
            {
                'nip': '199001011015011006',
                'name': 'Joko Widodo, S.Sos',
                'email': 'joko.widodo@sekolah.ac.id',
                'phone': '081234567895',
                'address': 'Jl. Sosial No. 987, Bogor',
                'subject': 'Sosiologi'
            }
        ]
        
        teachers = []
        for teacher_data in teachers_data:
            teacher = Teacher(**teacher_data)
            teachers.append(teacher)
            db.session.add(teacher)
        
        db.session.commit()
        
        # Create sample classes
        classes_data = [
            {'name': 'X-A', 'grade': 'X', 'teacher_id': teachers[0].id, 'academic_year': '2024/2025'},
            {'name': 'X-B', 'grade': 'X', 'teacher_id': teachers[1].id, 'academic_year': '2024/2025'},
            {'name': 'XI-A', 'grade': 'XI', 'teacher_id': teachers[2].id, 'academic_year': '2024/2025'},
            {'name': 'XI-B', 'grade': 'XI', 'teacher_id': teachers[3].id, 'academic_year': '2024/2025'},
            {'name': 'XII-A', 'grade': 'XII', 'teacher_id': teachers[4].id, 'academic_year': '2024/2025'},
            {'name': 'XII-B', 'grade': 'XII', 'teacher_id': teachers[5].id, 'academic_year': '2024/2025'}
        ]
        
        classes = []
        for class_data in classes_data:
            school_class = SchoolClass(**class_data)
            classes.append(school_class)
            db.session.add(school_class)
        
        db.session.commit()
        
        # Create sample students
        students_data = [
            # Class X-A students
            {'nisn': '0123456780', 'name': 'Ahmad Pratama', 'email': 'ahmad.pratama@email.com', 'phone': '081234567801', 'gender': 'Laki-laki', 'class_id': classes[0].id, 'address': 'Jl. Siswa No. 1, Jakarta'},
            {'nisn': '0123456781', 'name': 'Siti Nurhaliza', 'email': 'siti.nurhaliza@email.com', 'phone': '081234567802', 'gender': 'Perempuan', 'class_id': classes[0].id, 'address': 'Jl. Siswa No. 2, Jakarta'},
            {'nisn': '0123456782', 'name': 'Budi Setiawan', 'email': 'budi.setiawan@email.com', 'phone': '081234567803', 'gender': 'Laki-laki', 'class_id': classes[0].id, 'address': 'Jl. Siswa No. 3, Jakarta'},
            {'nisn': '0123456783', 'name': 'Rina Wati', 'email': 'rina.wati@email.com', 'phone': '081234567804', 'gender': 'Perempuan', 'class_id': classes[0].id, 'address': 'Jl. Siswa No. 4, Jakarta'},
            {'nisn': '0123456784', 'name': 'Andi Kusuma', 'email': 'andi.kusuma@email.com', 'phone': '081234567805', 'gender': 'Laki-laki', 'class_id': classes[0].id, 'address': 'Jl. Siswa No. 5, Jakarta'},
            
            # Class X-B students
            {'nisn': '0123456785', 'name': 'Maya Sari', 'email': 'maya.sari@email.com', 'phone': '081234567806', 'gender': 'Perempuan', 'class_id': classes[1].id, 'address': 'Jl. Siswa No. 6, Jakarta'},
            {'nisn': '0123456786', 'name': 'Dedi Irawan', 'email': 'dedi.irawan@email.com', 'phone': '081234567807', 'gender': 'Laki-laki', 'class_id': classes[1].id, 'address': 'Jl. Siswa No. 7, Jakarta'},
            {'nisn': '0123456787', 'name': 'Lisa Permata', 'email': 'lisa.permata@email.com', 'phone': '081234567808', 'gender': 'Perempuan', 'class_id': classes[1].id, 'address': 'Jl. Siswa No. 8, Jakarta'},
            {'nisn': '0123456788', 'name': 'Reza Pratama', 'email': 'reza.pratama@email.com', 'phone': '081234567809', 'gender': 'Laki-laki', 'class_id': classes[1].id, 'address': 'Jl. Siswa No. 9, Jakarta'},
            {'nisn': '0123456789', 'name': 'Indira Sari', 'email': 'indira.sari@email.com', 'phone': '081234567810', 'gender': 'Perempuan', 'class_id': classes[1].id, 'address': 'Jl. Siswa No. 10, Jakarta'},
            
            # Add more students for other classes...
            {'nisn': '0123456790', 'name': 'Fajar Nugroho', 'email': 'fajar.nugroho@email.com', 'phone': '081234567811', 'gender': 'Laki-laki', 'class_id': classes[2].id, 'address': 'Jl. Siswa No. 11, Jakarta'},
            {'nisn': '0123456791', 'name': 'Putri Maharani', 'email': 'putri.maharani@email.com', 'phone': '081234567812', 'gender': 'Perempuan', 'class_id': classes[2].id, 'address': 'Jl. Siswa No. 12, Jakarta'},
            {'nisn': '0123456792', 'name': 'Arif Hidayat', 'email': 'arif.hidayat@email.com', 'phone': '081234567813', 'gender': 'Laki-laki', 'class_id': classes[3].id, 'address': 'Jl. Siswa No. 13, Jakarta'},
            {'nisn': '0123456793', 'name': 'Sinta Dewi', 'email': 'sinta.dewi@email.com', 'phone': '081234567814', 'gender': 'Perempuan', 'class_id': classes[3].id, 'address': 'Jl. Siswa No. 14, Jakarta'},
            {'nisn': '0123456794', 'name': 'Bayu Aji', 'email': 'bayu.aji@email.com', 'phone': '081234567815', 'gender': 'Laki-laki', 'class_id': classes[4].id, 'address': 'Jl. Siswa No. 15, Jakarta'},
            {'nisn': '0123456795', 'name': 'Anita Sari', 'email': 'anita.sari@email.com', 'phone': '081234567816', 'gender': 'Perempuan', 'class_id': classes[4].id, 'address': 'Jl. Siswa No. 16, Jakarta'},
            {'nisn': '0123456796', 'name': 'Hendri Gunawan', 'email': 'hendri.gunawan@email.com', 'phone': '081234567817', 'gender': 'Laki-laki', 'class_id': classes[5].id, 'address': 'Jl. Siswa No. 17, Jakarta'},
            {'nisn': '0123456797', 'name': 'Ratna Sari', 'email': 'ratna.sari@email.com', 'phone': '081234567818', 'gender': 'Perempuan', 'class_id': classes[5].id, 'address': 'Jl. Siswa No. 18, Jakarta'},
        ]
        
        for student_data in students_data:
            student = Student(**student_data)
            db.session.add(student)
        
        # Create sample subjects
        subjects_data = [
            {'name': 'Matematika', 'code': 'MAT', 'description': 'Matematika Wajib', 'credits': 4},
            {'name': 'Bahasa Indonesia', 'code': 'BIN', 'description': 'Bahasa Indonesia', 'credits': 4},
            {'name': 'Bahasa Inggris', 'code': 'BIG', 'description': 'Bahasa Inggris', 'credits': 3},
            {'name': 'Fisika', 'code': 'FIS', 'description': 'Fisika', 'credits': 3},
            {'name': 'Kimia', 'code': 'KIM', 'description': 'Kimia', 'credits': 3},
            {'name': 'Biologi', 'code': 'BIO', 'description': 'Biologi', 'credits': 3},
            {'name': 'Sejarah', 'code': 'SEJ', 'description': 'Sejarah Indonesia', 'credits': 2},
            {'name': 'Geografi', 'code': 'GEO', 'description': 'Geografi', 'credits': 2},
            {'name': 'Ekonomi', 'code': 'EKO', 'description': 'Ekonomi', 'credits': 3},
            {'name': 'Sosiologi', 'code': 'SOS', 'description': 'Sosiologi', 'credits': 2},
            {'name': 'Seni Budaya', 'code': 'SBD', 'description': 'Seni Budaya', 'credits': 2},
            {'name': 'Pendidikan Jasmani', 'code': 'PJO', 'description': 'Pendidikan Jasmani dan Olahraga', 'credits': 2},
        ]
        
        for subject_data in subjects_data:
            subject = Subject(**subject_data)
            db.session.add(subject)
        
        db.session.commit()
        
        print("✅ Demo data berhasil dibuat!")
        print(f"   - {len(teachers_data)} guru")
        print(f"   - {len(classes_data)} kelas")
        print(f"   - {len(students_data)} siswa")
        print(f"   - {len(subjects_data)} mata pelajaran")
        print("\n🔑 Login admin:")
        print("   Username: admin")
        print("   Password: admin123")

if __name__ == '__main__':
    init_demo_data()