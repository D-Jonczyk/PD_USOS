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

  constructor(@Inject(DOCUMENT) public document: Document, public auth: AuthService, private http: HttpClient) {}

}
