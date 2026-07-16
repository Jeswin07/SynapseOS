import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { Loader2 } from "lucide-react";
import { AuthLayout } from "@/features/auth/components/AuthLayout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useRegister } from "@/hooks/useAuth";
import { ApiError } from "@/services/apiClient";

const schema = z.object({
  company_name: z.string().min(2, "Company name is required"),
  industry: z.string().min(2, "Industry is required"),
  full_name: z.string().min(2, "Your full name is required"),
  email: z.string().email("Enter a valid work email"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});

type FormValues = z.infer<typeof schema>;

export default function RegisterPage() {
  const navigate = useNavigate();
  const register_ = useRegister();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormValues>({ resolver: zodResolver(schema) });

  function onSubmit(values: FormValues) {
    register_.mutate(values, {
      onSuccess: () => {
        toast.success("Workspace created. Please sign in.");
        navigate("/login", { replace: true });
      },
      onError: (err) => {
        toast.error(err instanceof ApiError ? err.detail : "Unable to create your workspace.");
      },
    });
  }

  return (
    <AuthLayout title="Create your workspace" subtitle="Set up your organization's SynapseOS instance.">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="grid grid-cols-2 gap-3">
          <div className="space-y-1.5">
            <Label htmlFor="company_name">Company name</Label>
            <Input id="company_name" placeholder="Acme Corp" {...register("company_name")} />
            {errors.company_name && <p className="text-xs text-destructive">{errors.company_name.message}</p>}
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="industry">Industry</Label>
            <Input id="industry" placeholder="Retail" {...register("industry")} />
            {errors.industry && <p className="text-xs text-destructive">{errors.industry.message}</p>}
          </div>
        </div>
        <div className="space-y-1.5">
          <Label htmlFor="full_name">Full name</Label>
          <Input id="full_name" placeholder="Jane Doe" {...register("full_name")} />
          {errors.full_name && <p className="text-xs text-destructive">{errors.full_name.message}</p>}
        </div>
        <div className="space-y-1.5">
          <Label htmlFor="email">Work email</Label>
          <Input id="email" type="email" placeholder="you@company.com" {...register("email")} />
          {errors.email && <p className="text-xs text-destructive">{errors.email.message}</p>}
        </div>
        <div className="space-y-1.5">
          <Label htmlFor="password">Password</Label>
          <Input id="password" type="password" placeholder="••••••••" {...register("password")} />
          {errors.password && <p className="text-xs text-destructive">{errors.password.message}</p>}
        </div>
        <Button type="submit" className="w-full" disabled={register_.isPending}>
          {register_.isPending && <Loader2 className="h-4 w-4 animate-spin" />}
          Create workspace
        </Button>
      </form>
      <p className="text-center text-sm text-muted-foreground">
        Already have a workspace?{" "}
        <Link to="/login" className="font-medium text-primary hover:underline">
          Sign in
        </Link>
      </p>
    </AuthLayout>
  );
}
