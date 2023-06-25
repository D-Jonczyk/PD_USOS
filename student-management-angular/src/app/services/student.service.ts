import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {AuthService} from "@auth0/auth0-angular";
import {switchMap} from "rxjs";
import {Course, Enrollment} from "../models/models";

@Injectable({
  providedIn: 'root'
})
export class StudentService {
  constructor(private http: HttpClient, private auth: AuthService) { }

  getEnrolledCourses() {
    return this.auth.idTokenClaims$.pipe(
      switchMap((claims: any) =>
        this.http.get<Enrollment[]>(`http://localhost:8000/api/student-courses`, {
          headers: {
            Authorization: `Bearer ${claims.__raw}`
          }
        })
      )
    );
  }

  getCourses() {
    return this.auth.idTokenClaims$.pipe(
      switchMap((claims: any) =>
        this.http.get<Course[]>('http://localhost:8000/api/courses', {
          headers: {
            Authorization: `Bearer ${claims.__raw}`
          }
        })
      )
    );
  }

  enrollInCourse(courseId: number) {
    return this.auth.idTokenClaims$.pipe(
      switchMap((claims: any) =>
        this.http.post('http://localhost:8000/api/enroll', { course_id: courseId }, {
          headers: {
            Authorization: `Bearer ${claims.__raw}`
          }
        })
      )
    );
  }
}
