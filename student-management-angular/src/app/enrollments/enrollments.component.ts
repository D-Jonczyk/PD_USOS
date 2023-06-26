import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '@auth0/auth0-angular';
import {Course, Enrollment} from "../models/models";
import {StudentService} from "../services/student.service";

@Component({
  selector: 'app-enrollments',
  templateUrl: './enrollments.component.html',
  styleUrls: ['./enrollments.component.scss']
})
export class EnrollmentsComponent implements OnInit {
  enrolledCourses: Enrollment[] = [];
  availableCourses: Course[] = [];

  constructor(private studentService: StudentService) { }


  ngOnInit(): void {
    this.getEnrolledCourses();
    this.getAvailableCourses();
  }

  isEnrolled(courseId: number): boolean {
    return this.enrolledCourses.some(enrollment => enrollment.course_id === courseId);
  }

  getEnrolledCourses(): void {
    this.studentService.getEnrolledCourses().subscribe(
      courses => this.enrolledCourses = courses
    );
  }

  getAvailableCourses(): void {
    this.studentService.getCourses().subscribe(
      courses => this.availableCourses = courses
    );
  }

  enrollInCourse(courseId: number): void {
    this.studentService.enrollInCourse(courseId).subscribe(
      () => this.getEnrolledCourses()
    );
  }
}
