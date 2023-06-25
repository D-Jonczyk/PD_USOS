import {Component, OnInit} from '@angular/core';
import {Student} from "../models/models";
import {StudentService} from "../services/student.service";
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {Observable, switchMap} from "rxjs";
import {AuthService} from "@auth0/auth0-angular";

@Component({
  selector: 'app-student-list',
  templateUrl: './student-list.component.html',
  styleUrls: ['./student-list.component.scss']
})
export class StudentListComponent implements OnInit {

  students: Student[] | undefined;

  constructor(private http: HttpClient, public auth: AuthService) {}

  ngOnInit(): void {
    this.getStudents().subscribe(
      students => this.students = students
    );
  }

  getStudents(): Observable<Student[]> {
    return this.auth.idTokenClaims$.pipe(
      switchMap((claims: any) =>
        this.http.get<Student[]>('http://localhost:8000/api/students', {
          headers: new HttpHeaders({
            'Authorization': `Bearer ${claims.__raw}`
          })
        })
      )
    );
  }
}
