import {Component, OnInit} from '@angular/core';
import {AdminService} from "../services/admin.service";
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {throwError, catchError} from "rxjs";

class Department {
}

@Component({
  selector: 'app-admin-panel',
  templateUrl: './admin-panel.component.html',
  styleUrls: ['./admin-panel.component.scss']
})
export class AdminPanelComponent implements OnInit{
  departmentForm!: FormGroup;
  teacherForm!: FormGroup;

  errorMessage: string = '';
  successMessage: string = '';

  constructor(private adminService: AdminService) { }

  ngOnInit(): void {
    this.departmentForm = new FormGroup({
      name: new FormControl('', Validators.required),
      description: new FormControl('', Validators.required)
    });

    this.teacherForm = new FormGroup({
      name: new FormControl('', Validators.required),
      department: new FormControl('', Validators.required)
    });
  }

  onAddDepartment() {
    if (!this.departmentForm.valid) {
      return;
    }

    this.adminService.addDepartment(this.departmentForm.value).pipe(
      catchError(error => {
        this.errorMessage = 'Wystąpił błąd podczas dodawania wydziału. Proszę spróbować ponownie.';
        return throwError(error);
      })
    ).subscribe(response => {
      this.successMessage = 'Pomyślnie dodano nowy wydział.';
      this.departmentForm.reset();
      console.log(response);
    });
  }

}
