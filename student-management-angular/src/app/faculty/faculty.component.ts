import {Component, OnInit} from '@angular/core';
import {Observable} from "rxjs";
import {HttpClient} from "@angular/common/http";
import {DepartmentService} from "../services/department.service";

@Component({
  selector: 'app-faculty',
  templateUrl: './faculty.component.html',
  styleUrls: ['./faculty.component.scss']
})
export class FacultyComponent implements OnInit{
  departments: any[] = [];

  constructor(private departmentService: DepartmentService) { }

  ngOnInit(): void {
    this.departmentService.getDepartments().subscribe(
      (response: any) => this.departments = response,
      error => console.error(error)
    );
  }
}
