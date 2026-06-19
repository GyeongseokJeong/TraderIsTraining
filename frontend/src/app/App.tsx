import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { AppLayout } from '../widgets/layout/AppLayout';
import { SetupPage } from '../pages/setup/SetupPage';
import { TrainingPage } from '../pages/training/TrainingPage';
import { ReviewPage } from '../pages/review/ReviewPage';

const router = createBrowserRouter([{ element: <AppLayout />, children: [{ path: '/', element: <SetupPage /> }, { path: '/training/:sessionId', element: <TrainingPage /> }, { path: '/review/:sessionId', element: <ReviewPage /> }] }]);

export function App() { return <RouterProvider router={router} />; }
