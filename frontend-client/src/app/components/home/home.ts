import { Component, OnInit } from '@angular/core';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { CommonModule } from '@angular/common';
import { Api } from '../../services/api';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, MatSlideToggleModule],
  templateUrl: './home.html',
  styleUrl: './home.scss'
})
export class Home {
  message = '';

  constructor(private api: Api) { }

  ngOnInit(): void {
    this.api.getHomepage().subscribe({
      next: (data) => this.message = data.message,
      error: (err) => console.error(err)
    });
  }
}
