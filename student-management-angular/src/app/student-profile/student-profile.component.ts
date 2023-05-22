import { Component, Input } from '@angular/core';
import { Student } from '../models/student.model';
import { AuthService } from '@auth0/auth0-angular';

@Component({
  selector: 'app-student-profile',
  templateUrl: './student-profile.component.html',
  styleUrls: ['./student-profile.component.scss']
})
export class StudentProfileComponent {
  @Input() student: Student = {
    id: 0,
    first_name: '',
    last_name: '',
    email: '',
    major: '',
    gpa: '',
    username: '',
    date_of_birth: '',
    profilePicture: '',
    auth0_id: '',
  };

  constructor(public auth: AuthService) {}
}
