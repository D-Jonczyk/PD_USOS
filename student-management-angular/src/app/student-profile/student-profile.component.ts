import {Component, Input, OnInit} from '@angular/core';
import { Student } from '../models/student.model';
import { AuthService } from '@auth0/auth0-angular';
import {StudentService} from "../services/student.service";

@Component({
  selector: 'app-student-profile',
  templateUrl: './student-profile.component.html',
  styleUrls: ['./student-profile.component.scss']
})
export class StudentProfileComponent implements OnInit{
  @Input() student: Student = {
    id: 0,
    first_name: '',
    last_name: '',
    email: '',
    major: '',
    gpa: '',
    username: '',
    profilePicture: ''
  };

  constructor(public auth: AuthService, private studentService: StudentService) {}

  ngOnInit(): void {
    this.auth.user$.subscribe((user) => {
      if (user) {
        this.studentService.getStudent(user.sub).subscribe((student: Student) => {
          this.student = student;
        });
      }
    });
  }
}
