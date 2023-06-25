import {Component, OnInit} from '@angular/core';
import {TeacherService} from "../services/teacher.service";
import {AuthService} from "@auth0/auth0-angular";
import {switchMap} from "rxjs";
import {HttpClient} from "@angular/common/http";
import {Course, Student} from "../models/models";

@Component({
  selector: 'app-teacher-panel',
  templateUrl: './teacher-panel.component.html',
  styleUrls: ['./teacher-panel.component.scss']
})
export class TeacherPanelComponent implements OnInit{
  courses: any[] = [];
  course = {
    name: '',
    description: '',
    department: '', // replace with actual department ID
  };

  constructor(private teacherService: TeacherService, public auth: AuthService, private http: HttpClient) { }

  ngOnInit(): void {
    this.getTeacherCourses();
  }

  getTeacherCourses(): void {
    this.auth.idTokenClaims$.pipe(
      switchMap((claims: any) =>
        this.http.get<Course[]>('http://localhost:8000/api/teacher/courses', {
          headers: {
            Authorization: `Bearer ${claims.__raw}`
          }
        })
      )
    ).subscribe(courses => {
      this.courses = courses;
      this.courses.forEach(course => {
        this.auth.idTokenClaims$.pipe(
          switchMap((claims: any) =>
            this.http.get<Student[]>(`http://localhost:8000/api/teacher/course/${course.id}/students`, {
              headers: {
                Authorization: `Bearer ${claims.__raw}`
              }
            })
          )
        ).subscribe(students => {
          course.students = students;
        });
      });
    });
  }

  updateGrade(courseId: string, studentId: string, grade: string): void {
    this.teacherService.updateStudentGrade(courseId, studentId, grade).subscribe(response => {
      alert(response.detail);
      this.getTeacherCourses();
    });
  }
}
