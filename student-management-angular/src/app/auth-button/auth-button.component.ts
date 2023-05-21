import {Component, Inject, OnInit} from '@angular/core';
import { AuthService } from '@auth0/auth0-angular';
import { DOCUMENT } from '@angular/common';
import {HttpClient} from "@angular/common/http";
import {StudentService} from "../services/student.service";

@Component({
  selector: 'app-auth-button',
  template: `
    <ng-container *ngIf="auth.isAuthenticated$ | async; else loggedOut">
      <button class="btn btn-primary" (click)="auth.logout({ logoutParams: { returnTo: document.location.origin } })">
        <i class="fas fa-sign-out-alt"></i> Wyloguj
      </button>
    </ng-container>

    <ng-template #loggedOut>
      <button class="btn btn-primary" (click)="auth.loginWithRedirect()">
        <i class="fas fa-sign-in-alt"></i> Zaloguj
      </button>
    </ng-template>

  `,
  styles: [],
})
export class AuthButtonComponent {
  studentData: any = {
    // Set the student data here, such as auth0_id, first_name, last_name, etc.
  };
  constructor(@Inject(DOCUMENT) public document: Document, public auth: AuthService, private http: HttpClient,
              private studentService: StudentService) {}



  registerStudent() {
    this.studentService.addStudent(this.studentData).subscribe(
      (response) => {
        // Handle the success response here
        console.log('Student registered successfully:', response);
      },
      (error) => {
        // Handle the error response here
        console.error('Failed to register student:', error);
      }
    );
  }
}
