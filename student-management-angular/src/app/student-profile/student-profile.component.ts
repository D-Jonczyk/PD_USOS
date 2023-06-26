import {Component, Input, OnInit} from '@angular/core';
import {AuthService, IdToken} from '@auth0/auth0-angular';
import {StudentService} from "../services/student.service";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {FormBuilder, FormGroup} from "@angular/forms";
import {switchMap, catchError, filter, throwError} from "rxjs";

@Component({
  selector: 'app-student-profile',
  templateUrl: './student-profile.component.html',
  styleUrls: ['./student-profile.component.scss']
})
export class StudentProfileComponent implements OnInit{
  profileForm: FormGroup;
  errorMessage = '';
  successMessage = '';

  constructor(private fb: FormBuilder, private http: HttpClient, public auth: AuthService, private studentService: StudentService) {
    this.profileForm = this.fb.group({
      nickname: [''],
      picture: [''],
      given_name: [''],
      name: [''],
      auth0_id: ['']
    });
  }

  ngOnInit(): void {
    this.auth.idTokenClaims$.pipe(
      switchMap((claims: any) =>
        this.http.get('http://localhost:8000/api/profile', {
          headers: {
            Authorization: `Bearer ${claims.__raw}`
          }
        })
      )
    ).subscribe((response: any) => {
      this.profileForm.setValue({
        nickname: response.nickname,
        picture: response.picture,
        given_name: response.given_name,
        name: response.name,
        auth0_id: response.auth0_id
      });
    });
  }

  onSubmit(): void {
    this.auth.idTokenClaims$
      .pipe(
        filter((claims: any): claims is IdToken => claims !== null && claims !== undefined),
        switchMap((claims: IdToken) =>
          this.http.put('http://localhost:8000/api/profile', this.profileForm.value, {
            headers: {
              Authorization: `Bearer ${claims.__raw}`
            }
          }).pipe(
            catchError(error => {
              this.errorMessage = 'Wystąpił błąd podczas aktualizacji profilu. Proszę spróbować ponownie.';
              return throwError(error);
            })
          )
        )
      )
      .subscribe((response: any) => {
        this.successMessage = 'Profil został pomyślnie zaktualizowany.';
        console.log(response);
      }, error => {
        this.errorMessage = 'Wystąpił błąd podczas aktualizacji profilu. Proszę spróbować ponownie.';
      });
  }

}
