import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import { Observable } from 'rxjs';
import { Student } from '../models/student.model';

@Injectable({
  providedIn: 'root'
})
export class StudentService {
  private apiUrl = 'http://localhost:8000/api/check_student';
  private getStudentUrl = 'http://localhost:8000/api/students/';

  constructor(private http: HttpClient) { }

  getStudents(): Observable<Student[]> {
    return this.http.get<Student[]>(this.apiUrl);
  }

  getStudent(id: string | undefined): Observable<Student> {
    const url = `${this.getStudentUrl}${id}/`;
    return this.http.get<Student>(url);
  }

  addStudent(studentData: any) {
    const headers = new HttpHeaders().set('Content-Type', 'application/json');

    return this.http.post(this.apiUrl, studentData, { headers });
  }

  deleteStudent(id: number): Observable<Student> {
    const url = `${this.apiUrl}${id}/`;
    return this.http.delete<Student>(url);
  }

  updateStudent(student: Student | undefined): Observable<any> {
    // @ts-ignore
    const url = `${this.getStudentUrl}/${student.id}`; // Assuming the student object has an 'id' property
    return this.http.put(url, student);
  }
}
