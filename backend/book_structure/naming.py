"""
Naming logic for generating descriptive names based on book subject.

This module provides functions to generate descriptive names for modules,
chapters, and topics based on the book's subject matter.
"""

import random
from typing import List


def generate_module_names(subject: str, count: int = 5) -> List[str]:
    """
    Generate descriptive module names based on the book subject.

    Args:
        subject: The subject/topic of the book
        count: Number of module names to generate (default 5)

    Returns:
        List of descriptive module names
    """
    # Base module patterns based on subject
    patterns = [
        f"Introduction to {subject}",
        f"Fundamentals of {subject}",
        f"Core Concepts in {subject}",
        f"Advanced {subject} Techniques",
        f"Applications of {subject}",
        f"History and Evolution of {subject}",
        f"Practical {subject} Skills",
        f"Theory and Practice of {subject}",
        f"Modern {subject} Approaches",
        f"Foundations of {subject}",
        f"Essential {subject} Principles",
        f"Building with {subject}",
        f"Understanding {subject}",
        f"{subject} Patterns and Practices",
        f"Implementing {subject} Solutions",
    ]

    # Return a random selection of module names
    return random.sample(patterns, min(count, len(patterns)))


def generate_chapter_names(subject: str, module_context: str, count: int) -> List[str]:
    """
    Generate descriptive chapter names based on module context.

    Args:
        subject: The subject/topic of the book
        module_context: The context of the parent module
        count: Number of chapter names to generate

    Returns:
        List of descriptive chapter names
    """
    # Base chapter patterns
    patterns = [
        f"Overview of {module_context}",
        f"Basic Principles of {module_context}",
        f"Getting Started with {module_context}",
        f"Key Components of {module_context}",
        f"Setting up {module_context}",
        f"Working with {module_context}",
        f"Advanced Techniques in {module_context}",
        f"Troubleshooting {module_context}",
        f"Best Practices for {module_context}",
        f"Case Studies in {module_context}",
        f"Tools for {module_context}",
        f"Patterns in {module_context}",
        f"Common Mistakes in {module_context}",
        f"Optimizing {module_context}",
        f"Testing {module_context}",
        f"Deploying {module_context}",
        f"Security Considerations for {module_context}",
        f"Performance in {module_context}",
        f"Integration with {module_context}",
        f"Future of {module_context}",
        f"Review and Summary of {module_context}",
        f"Exercises in {module_context}",
        f"Examples of {module_context}",
        f"Building {module_context}",
        f"Designing {module_context}",
    ]

    # Return a random selection of chapter names
    return random.sample(patterns, min(count, len(patterns)))


def generate_topic_names(subject: str, chapter_context: str, count: int) -> List[str]:
    """
    Generate realistic topic names based on chapter scope.

    Args:
        subject: The subject/topic of the book
        chapter_context: The context of the parent chapter
        count: Number of topic names to generate

    Returns:
        List of realistic topic names
    """
    # Base topic patterns
    patterns = [
        f"What is {chapter_context}?",
        f"History of {chapter_context}",
        f"Benefits of {chapter_context}",
        f"Challenges with {chapter_context}",
        f"Basic {chapter_context} Concepts",
        f"Advanced {chapter_context} Concepts",
        f"Core Principles of {chapter_context}",
        f"Key Features of {chapter_context}",
        f"Syntax in {chapter_context}",
        f"Semantics in {chapter_context}",
        f"Implementation of {chapter_context}",
        f"Usage Examples for {chapter_context}",
        f"Code Samples for {chapter_context}",
        f"Configuration of {chapter_context}",
        f"Setup for {chapter_context}",
        f"Installation of {chapter_context}",
        f"Initialization of {chapter_context}",
        "Initialization Process",
        "Configuration Options",
        "Common Parameters",
        f"Error Handling in {chapter_context}",
        "Exception Management",
        "Debugging Techniques",
        "Performance Considerations",
        "Security Best Practices",
        "Testing Strategies",
        "Unit Testing",
        "Integration Testing",
        "Performance Testing",
        "Memory Management",
        "Threading and Concurrency",
        "Data Structures",
        "Algorithms",
        "Design Patterns",
        "Architecture Patterns",
        "Code Organization",
        "Naming Conventions",
        "Documentation Standards",
        "Code Review Guidelines",
        "Version Control Practices",
        "Deployment Strategies",
        "Monitoring and Logging",
        "Troubleshooting Common Issues",
        "Performance Optimization",
        "Memory Optimization",
        "Code Optimization",
        "Resource Management",
        "Error Recovery",
        "Fault Tolerance",
        "Scalability Considerations",
        "Maintenance Guidelines",
    ]

    # Return a random selection of topic names
    return random.sample(patterns, min(count, len(patterns)))


def generate_book_structure_names(subject: str) -> dict:
    """
    Generate a complete set of names for a book structure.

    Args:
        subject: The subject/topic of the book

    Returns:
        Dictionary containing module, chapter, and topic names
    """
    # Generate module names
    module_names = generate_module_names(subject)

    result = {"modules": []}

    for i, module_name in enumerate(module_names):
        # Generate chapter names for this module (5-10 chapters)
        chapter_count = random.randint(5, 10)
        chapter_names = generate_chapter_names(subject, module_name, chapter_count)

        modules_chapters = []
        for j, chapter_name in enumerate(chapter_names):
            # Generate topic names for this chapter (12-20 topics)
            topic_count = random.randint(12, 20)
            topic_names = generate_topic_names(subject, chapter_name, topic_count)

            modules_chapters.append({"name": chapter_name, "topics": topic_names})

        result["modules"].append({"name": module_name, "chapters": modules_chapters})

    return result
