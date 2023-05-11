import {Component, OnInit} from '@angular/core';
import {Student} from "../models/student.model";
import {StudentService} from "../services/student.service";

@Component({
  selector: 'app-student-list',
  templateUrl: './student-list.component.html',
  styleUrls: ['./student-list.component.scss']
})
export class StudentListComponent implements OnInit{

  students: Student[] | undefined;

  constructor(private studentService: StudentService) { }

  ngOnInit(): void {
    this.getStudents();
  }

  getStudents(): void {
    this.studentService.getStudents().subscribe((students: Student[] | undefined) => this.students = students);
  }
}
