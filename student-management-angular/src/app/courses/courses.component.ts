import { Component } from '@angular/core';
import {CourseService} from "../course.service";
import {finalize} from "rxjs";

@Component({
  selector: 'app-courses',
  templateUrl: './courses.component.html',
  styleUrls: ['./courses.component.scss']
})
export class CoursesComponent {
  courses: any[] = [];
  course = {
    name: '',
    description: '',
    department: '', // replace with actual department ID
    instructor: '',
  };
  isLoading: boolean = false;
  message: string = '';

  constructor(private courseService: CourseService) {}

  ngOnInit() {
    this.loadCourses();
  }

  loadCourses() {
    this.courseService.getCourses()
      .subscribe(
        (data: any[]) => {
          this.courses = data;
        },
        error => {
          console.log(error);
        });
  }

  createCourse() {
    this.isLoading = true; // Start loading

    this.courseService.createCourse(this.course)
      .pipe(
        finalize(() => {
          this.isLoading = false; // End loading regardless of the outcome
        })
      )
      .subscribe(
        response => {
          this.loadCourses(); // Refresh the list after a new course is created
          this.message = 'Kurs pomyślnie stworzony!'; // Display success message
        },
        error => {
          console.log(error);
          this.message = 'Wystąpił błąd przy tworzeniu kursu.'; // Display error message
        }
      );
  }

  // Add other methods for update, delete etc.
}
